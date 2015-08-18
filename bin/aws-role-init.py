#!/usr/bin/env python

# aws-role-init - assume an AWS role and output shell variables that will allow
# you to assume the role.

import boto
import boto.sts
import argparse
import sys

class AwsRoleInit:
    """aws-role-init - assume an AWS role and output shell variables"""

    role_session_name = ''
    role_arn = ''
    mfa_serial = None
    mfa_token = None
    sts_connection = None
    sts_session = None

    def __init__(self, role_session_name, role_arn, mfa_serial=None, mfa_token=None):
        """Set up boto, etc to get the object ready"""
        try:
            self.sts_connection = boto.sts.STSConnection()
        except boto.exception.NoAuthHandlerFound:
            print """\
            ERROR: AWS config not set up properly.
            See http://code.google.com/p/boto/wiki/BotoConfig or
            http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
            for details on how to set up boto and the AWS cli for use.
            """
            sys.exit(1)
        self.role_session_name = role_session_name
        self.role_arn = role_arn
        self.mfa_serial = mfa_serial
        self.mfa_token = mfa_token

    def assume_role(self):
        """Assume the supplied role and populate the session data."""
        self.sts_session = self.sts_connection.assume_role(self.role_arn,
            self.role_session_name, mfa_serial_number=self.mfa_serial, mfa_token=self.mfa_token)

    def output_env(self):
        """Output the session data as environment variables (bash only currently)"""
        print """\
        export AWS_ACCESS_KEY_ID={0}
        export AWS_SECRET_ACCESS_KEY={1}
        export AWS_SESSION_TOKEN={2}
        """.format(self.sts_session['Credentials']['AccessKeyId'],
            self.sts_session['Credentials']['SecretAccessKey'],
            self.sts_session['Credentials']['SessionToken'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='aws-shell-init: assume an AWS role and set environment variables')
    parser.add_argument('--role-session-name', action='store', nargs=1, required=True,
        help='The name to give to the session')
    parser.add_argument('--role-arn', action='store', nargs=1, required=True,
        help='The ARN of the role to assume')
    parser.add_argument('--serial-number', action='store', nargs=1, required=False,
        help='The ARN of the MFA device being used', default=None)
    parser.add_argument('--token-code', action='store', nargs=1, required=False,
        help='The ARN of the MFA device being used', default=None)

    args = parser.parse_args()

    if ((args.serial_number != None and args.token_code == None)
            or (args.serial_number == None and args.token_code != None)):
        print 'ERROR: --serial-number and --token-code must be defined together'
        sys.exit(1)

    ari = AwsRoleInit(args.role_session_name, args.role_arn,
        args.serial_number, args.token_code)
    ari.assume_role()
    ari.output_env()
