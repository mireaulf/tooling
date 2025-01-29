from mypy_boto3_rds.type_defs import DBInstanceTypeDef

from aws.clients.base_client import BaseClient
from aws.clients.log_group import CWLogGroupClient, LOG_GROUP_RDS_PREFIX
from aws.clients.rds import RDS


class CreateAuditLogGroups(BaseClient): # rename
    def __init__(self, rds_client: RDS, cw_log_group_client: CWLogGroupClient, dry_run: bool = True):
        super().__init__(dry_run)
        self.rds_client = rds_client
        self.cw_log_group_client = cw_log_group_client

    def execute(self, retention_in_days: int, do_once: bool = True) -> None:
        log_groups_to_create, log_groups_to_edit = self._get_audit_log_groups_to_create()
        for log_group_name in log_groups_to_edit:
            self.cw_log_group_client.update_log_group_retention(log_group_name, retention_in_days)
            if do_once:
                self.info("Stopping after one iteration")
                break

        for log_group_name, db_instance in log_groups_to_create.items():
            self.cw_log_group_client.create_log_group(log_group_name, {
                "coveo_billing": "security__mt__dblogs",
                "coveo_team_name": "security",
                "uam_team": "security",
            })
            self.cw_log_group_client.update_log_group_retention(log_group_name, retention_in_days)
            self.rds_client.enable_audit_log(db_instance)
            # enable audit log parameters on db instance/cluster parameter group
            if do_once:
                self.info("Stopping after one iteration")
                break


    def _get_audit_log_groups_to_create(self) -> (dict[
        # TODO handle postgresl log
        str, DBInstanceTypeDef], set[str]):
        log_groups = {log_group["logGroupName"]: log_group for log_group in self.cw_log_group_client.list_log_groups() if
                      log_group["logGroupName"].startswith(LOG_GROUP_RDS_PREFIX)}
        log_groups_to_create = dict()
        log_groups_to_edit = set()
        db_instances = self.rds_client.list_db_instances()
        for db_instance in db_instances:
            log_group_name = LOG_GROUP_RDS_PREFIX + "instance/" + db_instance.get("DBInstanceIdentifier")
            if db_cluster_id := db_instance.get("DBClusterIdentifier"):
                log_group_name = LOG_GROUP_RDS_PREFIX + "cluster/" + db_cluster_id

            if db_instance.get("Engine") == "postgres":
                self.warn(f"Postgres audit log not supported yet for {db_instance['DBInstanceIdentifier']}")
                continue

            log_group_name = f"{log_group_name}/audit"
            if log_group_name in log_groups:
                log_groups_to_edit.add(log_group_name)
                continue
            log_groups_to_create[log_group_name] = db_instance
        return log_groups_to_create, log_groups_to_edit