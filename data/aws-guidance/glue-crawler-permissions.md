# Glue Crawler Permissions

## Purpose

This document explains common permission issues when an AWS Glue crawler scans data stored in Amazon S3 and creates or updates metadata tables in the AWS Glue Data Catalog.

It is intended for troubleshooting scenarios where a crawler fails with `AccessDenied`, creates no tables, or cannot read encrypted S3 objects.

## Common symptoms

- The crawler fails with `AccessDenied`.
- The crawler cannot read files from the S3 source path.
- The crawler runs successfully but creates no table.
- The crawler creates a table, but the schema is incomplete or incorrect.
- The crawler fails when scanning S3 objects encrypted with AWS KMS.
- The crawler can list the bucket but cannot read individual objects.
- The crawler works for one S3 prefix but fails for another prefix.

## Root causes

- The Glue crawler IAM role does not have `s3:ListBucket` permission on the bucket.
- The Glue crawler IAM role does not have `s3:GetObject` permission on the target S3 prefix.
- The S3 bucket policy explicitly denies access to the crawler role.
- The S3 objects are encrypted with SSE-KMS, but the crawler role does not have `kms:Decrypt`.
- The KMS key policy does not allow the crawler role to use the key.
- The crawler is configured with the wrong IAM role.
- The crawler points to the wrong S3 path or an empty prefix.
- The crawler cannot infer schema because files are empty, corrupted, or inconsistent.
- The Glue Data Catalog database does not exist or the role lacks Glue catalog permissions.
- Lake Formation permissions block access to the database, table, or registered S3 location.

## Required permissions or configuration

The crawler role should usually have permissions for:

- `glue:*` actions required for crawler execution and catalog updates
- `s3:ListBucket` on the source bucket
- `s3:GetObject` on the source object prefix
- `kms:Decrypt` if the S3 objects are encrypted with SSE-KMS
- Glue Data Catalog permissions to create or update databases and tables
- Lake Formation permissions if the data lake is governed by Lake Formation

Example S3 bucket-level permission:

    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::example-bucket"
    }

Example S3 object-level permission:

    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::example-bucket/example-prefix/*"
    }

Example KMS permission:

    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:eu-central-1:123456789012:key/example-key-id"
    }

## Troubleshooting checklist

1. Confirm which IAM role the crawler is using.
2. Check whether the role has `s3:ListBucket` on the bucket.
3. Check whether the role has `s3:GetObject` on the exact S3 prefix.
4. Check whether the bucket policy denies access to the role.
5. Check whether the source objects are encrypted with SSE-KMS.
6. If KMS is used, confirm that the role has `kms:Decrypt`.
7. Check the KMS key policy and verify that it allows the crawler role.
8. Confirm that the S3 prefix contains valid files.
9. Confirm that the files have a consistent format and schema.
10. Check whether Lake Formation is enabled for the database or S3 location.
11. If Lake Formation is enabled, grant the required database, table, and data location permissions.
12. Rerun the crawler and review CloudWatch logs for the exact error message.

## Example user questions

- Why does my Glue crawler fail with `AccessDenied` on S3?
- Why can the crawler list the bucket but not read the files?
- What permissions does a Glue crawler need to read KMS-encrypted S3 data?
- Why does my crawler run successfully but create no table?
- How do I troubleshoot a Glue crawler that cannot access a specific S3 prefix?
- Does a Glue crawler need Lake Formation permissions?
