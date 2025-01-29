import boto3

from aws.clients.log_group import CWLogGroupClient, LOG_GROUP_RDS_PREFIX
from aws.clients.rds import RDS
from aws.commands.create_audit_log_groups import CreateAuditLogGroups

dry_run = True
do_once = False
rds_client = RDS(boto3.client("rds"))
cw_log_group_client = CWLogGroupClient(boto3.client("logs"), dry_run)

CreateAuditLogGroups(rds_client, cw_log_group_client, dry_run).execute(180, do_once=do_once)
