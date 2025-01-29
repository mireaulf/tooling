from typing import Iterator

from mypy_boto3_logs.client import CloudWatchLogsClient
from mypy_boto3_logs.type_defs import LogGroupTypeDef

from aws.clients.base_client import BaseClient

LOG_GROUP_RDS_PREFIX = "/aws/rds/"

class CWLogGroupClient(BaseClient):
    def __init__(self, boto3_cw: CloudWatchLogsClient, dry_run: bool = True) -> None:
        super().__init__(dry_run)
        self.client = boto3_cw

    def list_log_groups(self) -> Iterator[LogGroupTypeDef]:
        paginator = self.client.get_paginator("describe_log_groups")
        for page in paginator.paginate():
            for log_group in page["logGroups"]:
                yield log_group

    def create_log_group(self, log_group_name: str, tags: dict[str, str]) -> None:
        if self.dry_run:
            self.warn(f"Would create log group {log_group_name}")
            return
        resp = self.client.create_log_group(logGroupName=log_group_name, tags=tags, logGroupClass="INFREQUENT_ACCESS")
        if self.is_success(resp):
            self.log_add(f"Log group {log_group_name} created successfully")

    def update_log_group_retention(self, log_group_name: str, retention_in_days: int) -> None:
        if self.dry_run:
            self.warn(f"Would update log group {log_group_name} retention policy to {retention_in_days} days")
            return
        resp = self.client.put_retention_policy(logGroupName=log_group_name, retentionInDays=retention_in_days)
        if self.is_success(resp):
            self.log_add(f"Log group {log_group_name} retention policy updated successfully to {retention_in_days} days")