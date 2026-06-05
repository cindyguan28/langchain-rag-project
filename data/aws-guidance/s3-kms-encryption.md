# S3 KMS Encryption

## Purpose

This document explains common access issues when Amazon S3 objects are encrypted with AWS Key Management Service keys.

It is intended for troubleshooting scenarios where a user, role, Glue crawler, Athena query, or QuickSight dashboard has S3 access but still cannot read encrypted objects.

## Common symptoms

- A principal can list S3 objects but cannot read them.
- `s3:GetObject` is allowed, but access still fails.
- Athena query fails on encrypted S3 data.
- Glue crawler fails with `kms:Decrypt AccessDenied`.
- QuickSight cannot load data from Athena or S3.
- Cross-account access works for non-encrypted files but fails for encrypted files.
- Writing encrypted objects fails with a KMS permission error.
- The error message mentions `kms:Decrypt`, `kms:GenerateDataKey`, or key policy.

## Root causes

- The principal has S3 permissions but lacks KMS permissions.
- The KMS key policy does not allow the principal or account to use the key.
- The IAM policy allows KMS usage, but the key policy does not trust the account or principal.
- The S3 bucket uses a customer-managed KMS key.
- Cross-account access is missing permissions in the KMS key policy.
- The principal can read from S3 but cannot decrypt the object.
- The principal can write to S3 but cannot generate a data key for encryption.
- The service role used by Glue, Athena, Lake Formation, or QuickSight lacks KMS access.
- There is an explicit deny in IAM, bucket policy, service control policy, or key policy.

## Required permissions or configuration

For reading SSE-KMS encrypted S3 objects, the principal usually needs:

- `s3:GetObject` on the object path
- `s3:ListBucket` on the bucket if listing is required
- `kms:Decrypt` on the KMS key
- A KMS key policy that allows the principal or the principal's account to use the key

For writing SSE-KMS encrypted S3 objects, the principal usually needs:

- `s3:PutObject` on the object path
- `kms:GenerateDataKey`
- Sometimes `kms:Encrypt`
- A KMS key policy that allows the principal or account to use the key

For troubleshooting AWS service access:

- Identify the actual service role.
- Grant KMS permissions to the actual role used by the service.
- Check both IAM policy and KMS key policy.
- For cross-account access, update the KMS key policy in the key-owning account.

Example read permissions:

    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:eu-central-1:123456789012:key/example-key-id"
    }

Example write permissions:

    {
      "Effect": "Allow",
      "Action": [
        "kms:GenerateDataKey",
        "kms:Encrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:eu-central-1:123456789012:key/example-key-id"
    }

## Troubleshooting checklist

1. Confirm whether the S3 object is encrypted with SSE-KMS.
2. Identify the exact KMS key used for encryption.
3. Identify the principal or service role that is trying to access the object.
4. Check whether the principal has `s3:GetObject`.
5. Check whether the principal has `kms:Decrypt`.
6. Check whether the KMS key policy allows the principal or account.
7. Check for explicit denies in IAM policies, bucket policies, SCPs, or key policies.
8. For Glue, confirm the crawler or job role.
9. For Athena, confirm the querying role and query result location encryption.
10. For QuickSight, confirm whether the failure comes from QuickSight permissions, Athena permissions, or S3/KMS permissions.
11. For Lake Formation, confirm the role used for the registered S3 location.
12. For cross-account access, update both S3 bucket policy and KMS key policy.
13. Retry with a small test object to isolate whether the issue is S3, KMS, or the query engine.

## Example user questions

- Why do I get `kms:Decrypt AccessDenied` although I have S3 access?
- What permissions are required to read SSE-KMS encrypted S3 objects?
- Why does my Glue crawler fail on encrypted S3 data?
- Why does Athena fail only for encrypted files?
- How do I configure KMS permissions for cross-account S3 access?
- What is the difference between S3 permission and KMS permission?
- Which role needs KMS permissions when an AWS service reads encrypted S3 data?
