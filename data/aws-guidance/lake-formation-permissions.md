# Lake Formation Permissions

## Purpose

This document explains how AWS Lake Formation permissions interact with IAM, Glue Data Catalog, Amazon S3, Athena, and KMS.

It is intended for troubleshooting cases where IAM permissions appear correct, but users or services still cannot access databases, tables, columns, or S3 data governed by Lake Formation.

## Common symptoms

- A user can see a Glue database but cannot query its tables.
- A user can see a table but cannot access all columns.
- Athena query fails even though the IAM role has S3 permissions.
- A Glue crawler or ETL job cannot access a registered S3 location.
- A principal cannot create a table in a database.
- A principal cannot access data in a Lake Formation governed location.
- Access works in one account but fails in a cross-account setup.
- Access fails only for encrypted S3 locations.
- Data is visible in the catalog, but the query engine cannot read the underlying files.

## Root causes

- The principal has IAM permissions but lacks Lake Formation database or table permissions.
- The principal has table permissions but lacks data location permissions.
- The S3 location is registered in Lake Formation, and access is controlled by Lake Formation.
- The IAMAllowedPrincipals setting is not configured as expected.
- Column-level permissions restrict access to specific columns.
- Row-level or cell-level filters restrict the returned data.
- The S3 bucket policy does not allow the Lake Formation service role or the querying principal.
- The registered S3 location uses a role that lacks access to the bucket.
- The S3 data is encrypted with KMS, but the required KMS permissions are missing.
- Cross-account resource sharing is incomplete or misconfigured.

## Required permissions or configuration

Lake Formation access usually involves multiple layers:

- IAM permissions to call AWS services and APIs
- Lake Formation database permissions
- Lake Formation table permissions
- Lake Formation column permissions if column-level security is used
- Lake Formation data location permissions for creating or altering tables that point to S3
- S3 bucket and object permissions
- KMS key permissions for encrypted data
- AWS RAM configuration for cross-account sharing

Common Lake Formation permissions include:

- `DESCRIBE` on databases or tables
- `SELECT` on tables or columns
- `CREATE_TABLE` on a database
- `ALTER` for modifying table metadata
- Data location permission for registered S3 locations

Important concept:

IAM controls whether a principal can call APIs. Lake Formation controls whether the principal is allowed to access catalog resources and governed data. Both layers may be required.

## Troubleshooting checklist

1. Identify the principal that is trying to access the data.
2. Check whether the database or table is governed by Lake Formation.
3. Verify IAM permissions for Athena, Glue, or the relevant AWS service.
4. Verify Lake Formation database permissions.
5. Verify Lake Formation table permissions.
6. Check whether column-level permissions restrict the requested columns.
7. Check whether row-level or cell-level filters apply.
8. Check whether the S3 location is registered in Lake Formation.
9. Verify data location permissions if the principal creates or alters tables.
10. Check the IAM role used for the registered S3 location.
11. Confirm that the S3 bucket policy allows the required access.
12. If data is encrypted, check `kms:Decrypt` and the KMS key policy.
13. For cross-account access, check AWS RAM sharing and recipient account permissions.
14. Test access with a minimal query, such as selecting one allowed column with `LIMIT 10`.

## Example user questions

- Why does Athena fail even though my IAM role has S3 access?
- What is the difference between IAM permissions and Lake Formation permissions?
- Why can I see a table but not query it?
- Why can I query some columns but not others?
- What are Lake Formation data location permissions?
- Why does access fail for an encrypted S3 location registered in Lake Formation?
- How do I troubleshoot cross-account Lake Formation access?
