aws-role-init.py
=================

Use this script to assume an AWS role, and then output shell variables that you
can use to perform AWS tasks using a specific role.

Requirements
-------------

 * Python (2.7+)
 * boto3 (https://github.com/boto/boto3)
 * AWS CLI (recommended, not needed - https://github.com/aws/aws-cli)

Usage
------

Currently only bash is supported, but other shells may be added if need be.

The script outputs environment variables, so to use it effectively, run
the script thru an `eval` statement:

```
eval `./aws-role-init.py --role-session-name sandbox-session \
--role-arn arn:aws:iam::123456789012:role/RoleName \
--serial-number arn:aws:iam::123456789012:mfa/mfaDevice \
--token-code 123456`
```

Note that the MFA options (`--serial-number` and `--token-code`) are optional.

After this is done, the environment should be set up properly for use with most
AWS CLI or SDK-related tasks.

Blame
------

Chris Marchesi (<cmarchesi@paybyphone.com>)
