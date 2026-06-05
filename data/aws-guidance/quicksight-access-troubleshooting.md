# QuickSight Access Troubleshooting

## Purpose

This document explains common access issues in Amazon QuickSight, especially when users cannot see dashboards, cannot open embedded dashboards, lose access to shared folders, or encounter permission errors with datasets and data sources.

It is intended for troubleshooting dashboard visibility, folder sharing, dataset access, and embedded analytics access.

## Common symptoms

- A user cannot see a dashboard in the dashboard list.
- A user receives a permission error when opening a dashboard.
- An embedded dashboard does not load.
- A dashboard link works for one user but not another.
- A dashboard is visible, but visuals fail to load.
- A user can access the dashboard but not the underlying dataset.
- A shared folder disappeared from the user's view.
- A user has QuickSight access but not access to a specific dashboard.
- A user has AWS console access but is not provisioned correctly in QuickSight.
- A group has access, but one expected user still cannot see the asset.

## Root causes

- The dashboard was not shared with the user or the user's group.
- The dashboard was shared, but the dataset or data source was not accessible.
- The user is not provisioned as a QuickSight user.
- The user belongs to the wrong namespace.
- The dashboard is stored in a shared folder, but folder permissions were not granted correctly.
- The user has viewer access but needs author or owner permissions for editing.
- The dashboard link only works for users who already have permission.
- Group membership is outdated or missing.
- The embedded dashboard integration uses the wrong user identity, namespace, or session configuration.
- The dashboard depends on Athena, S3, or another AWS service where permissions are missing.
- The dataset uses row-level security or column-level security that filters out the expected data.

## Required permissions or configuration

Typical areas to check:

- QuickSight user provisioning
- QuickSight namespace
- Dashboard sharing permissions
- Shared folder permissions
- Group membership
- Dataset permissions
- Data source permissions
- Row-level security configuration
- Column-level security configuration
- Embedded dashboard session settings
- AWS resource permissions, for example Athena or S3 access

For dashboard access:

- The dashboard must be shared directly with the user or with a group that contains the user.
- The user must have the correct permission level.
- For links, the user still needs permission to access the dashboard.

For shared folder access:

- The shared folder must be shared with the user or group.
- The permission level should match the expected activity, such as viewer, contributor, or owner.

For dataset-related issues:

- The dataset must be shared with the right principals if direct dataset access is required.
- The data source must be valid and accessible.
- Underlying Athena, S3, Lake Formation, or KMS permissions may also be required.

## Troubleshooting checklist

1. Confirm whether the user is provisioned in QuickSight.
2. Confirm the user's QuickSight namespace.
3. Check whether the dashboard is shared with the user directly.
4. Check whether the dashboard is shared with a group.
5. Verify that the user is actually a member of the expected group.
6. Check whether the dashboard is located inside a shared folder.
7. If a shared folder is used, check the folder permissions.
8. Open the dashboard as an admin or owner and review sharing settings.
9. Check whether the dashboard visuals fail because of dataset or data source permissions.
10. Check whether the dataset uses row-level security or column-level security.
11. If the dashboard uses Athena, verify Athena, S3, Lake Formation, and KMS access.
12. For embedded dashboards, verify the user identity, namespace, session tags, and allowed domains.
13. Ask the user whether they access the dashboard through the QuickSight console, Data Portal, or an embedded link.
14. Test with a known working user and compare group membership and permissions.

## Example user questions

- Why can one user see a QuickSight dashboard but another user cannot?
- Why does an embedded QuickSight dashboard not load?
- What should I check if a QuickSight shared folder disappeared?
- Does a dashboard link work without dashboard permissions?
- Why do QuickSight visuals fail although the dashboard opens?
- How do I troubleshoot QuickSight dashboard access through groups?
- What is the difference between dashboard permission and dataset permission?
