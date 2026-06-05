# Athena Query Issues

## Purpose

This document describes common query failures in Amazon Athena, especially issues related to S3 access, Glue Data Catalog metadata, partition configuration, Lake Formation, and KMS-encrypted data.

It is intended for troubleshooting SQL queries that fail even though the table appears to exist in the Data Catalog.

## Common symptoms

- Athena query fails with `AccessDenied`.
- Athena query fails with `HIVE_CURSOR_ERROR`.
- Athena query fails with `HIVE_BAD_DATA`.
- Athena cannot read files from an S3 location.
- Athena can see the table but cannot query the data.
- Athena query returns no results although files exist in S3.
- Athena fails when querying KMS-encrypted data.
- Athena complains about invalid table properties.
- Athena returns schema mismatch errors.
- Athena query fails after partitions are added manually.

## Root causes

- The querying principal does not have permission to read the S3 source data.
- The Athena query result location is not configured or not writable.
- The S3 bucket policy denies access to the user, role, or Athena workgroup context.
- The table location in the Glue Data Catalog points to the wrong S3 path.
- The table schema does not match the actual file format.
- The table is configured as Parquet, but the files are CSV, JSON, or another format.
- The data contains values that do not match the declared column types.
- Partitions are missing, outdated, or pointing to incorrect S3 locations.
- Partition projection is configured incorrectly.
- The source data is encrypted with KMS, but the principal lacks `kms:Decrypt`.
- Lake Formation permissions block access to the database, table, columns, or data location.
- The file was deleted or changed while Athena was reading it.

## Required permissions or configuration

The querying user or role usually needs:

- Permission to run Athena queries
- Permission to read metadata from the Glue Data Catalog
- `s3:GetObject` on the source data path
- `s3:ListBucket` on the source bucket
- `s3:PutObject` and related permissions on the Athena query result bucket
- `kms:Decrypt` if source data or query results are encrypted with SSE-KMS
- Lake Formation permissions if the table is governed by Lake Formation

Important configuration areas:

- Athena workgroup
- Query result location
- Glue Data Catalog table location
- Table schema and file format
- Partition metadata
- S3 bucket policy
- KMS key policy
- Lake Formation permissions

## Troubleshooting checklist

1. Read the exact Athena error message.
2. Confirm which user or IAM role is running the query.
3. Check the Athena workgroup and query result location.
4. Confirm that the user or role can write query results to the result bucket.
5. Check the Glue table location and verify that the S3 path exists.
6. Confirm that the user or role has `s3:GetObject` on the source data.
7. Confirm that the user or role has `s3:ListBucket` on the source bucket.
8. Check whether the source objects are encrypted with SSE-KMS.
9. If KMS is used, verify `kms:Decrypt` and the KMS key policy.
10. Compare the Glue table schema with the actual file format.
11. Check whether partition metadata is correct.
12. If partition projection is used, validate the projection properties and S3 location template.
13. Check whether Lake Formation governs the database or table.
14. If Lake Formation is enabled, verify database, table, column, and data location permissions.
15. Rerun the query with a small `LIMIT` to isolate the problem.

## Example user questions

- Why does my Athena query fail with `AccessDenied`?
- Why can I see a table in Athena but not query it?
- What permissions are required for Athena to query S3 data?
- Why does Athena fail on KMS-encrypted data?
- How do I troubleshoot `HIVE_BAD_DATA`?
- Why does Athena return no rows although files exist in S3?
- How do Lake Formation permissions affect Athena queries?
