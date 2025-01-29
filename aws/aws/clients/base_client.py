
class BaseClient:
    def __init__(self, dry_run: bool) -> None:
        self.dry_run = dry_run

    @staticmethod
    def is_success(response: dict) -> bool:
        return response["ResponseMetadata"]["HTTPStatusCode"] == 200

    @staticmethod
    def warn(message: str) -> None:
        print(f"[!] {message}")

    @staticmethod
    def info(message: str) -> None:
        print(f"[*] {message}")

    @staticmethod
    def log_add(message: str) -> None:
        print(f"[+] {message}")

    @staticmethod
    def log_remove(message: str) -> None:
        print(f"[-] {message}")