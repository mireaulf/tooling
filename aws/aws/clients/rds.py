from typing import Iterator

from mypy_boto3_rds.client import RDSClient
from mypy_boto3_rds.type_defs import DBInstanceTypeDef

from aws.clients.base_client import BaseClient


class RDS(BaseClient):
    def __init__(self, boto3_rds: RDSClient, dry_run: bool = True) -> None:
        super().__init__(dry_run)
        self.client = boto3_rds

    def list_db_instances(self) -> Iterator[DBInstanceTypeDef]:
        paginator = self.client.get_paginator("describe_db_instances")
        for page in paginator.paginate():
            for instance in page["DBInstances"]:
                yield instance

    def enable_audit_log(self, db_instance: DBInstanceTypeDef) -> None:
        db_engine = db_instance["Engine"]
        if db_engine in ["mysql", "aurora-mysql"]:
            if self.dry_run:
                self.warn(f"Would enable audit log on {db_instance['DBInstanceIdentifier']}")
                return

            current_log_types = db_instance.get("EnabledCloudwatchLogsExports", [])
            log_types = current_log_types + ["audit"]
            resp = self.client.modify_db_instance(
                DBInstanceIdentifier=db_instance["DBInstanceIdentifier"],
                CloudwatchLogsExportConfiguration={
                    'EnableLogTypes': log_types
                },
                ApplyImmediately=True
            )
            if self.is_success(resp):
                self.log_add(f"Audit log enabled on {db_instance['DBInstanceIdentifier']}")
            return

        if db_engine in ["postgres", "aurora-postgresql"]:
            if self.dry_run:
                self.warn(f"Would enable audit log on {db_instance['DBInstanceIdentifier']}")
                return

            current_log_types = db_instance.get("EnabledCloudwatchLogsExports", [])
            log_types = current_log_types + ["postgresql"]
            resp = self.client.modify_db_instance(
                DBInstanceIdentifier=db_instance["DBInstanceIdentifier"],
                CloudwatchLogsExportConfiguration={
                    'EnableLogTypes': log_types
                },
                ApplyImmediately=True
            )
            if self.is_success(resp):
                self.log_add(f"Audit log enabled on {db_instance['DBInstanceIdentifier']}")
            return

        self.warn(f"Audit log not supported for engine {db_engine} for {db_instance['DBInstanceIdentifier']}")
        return