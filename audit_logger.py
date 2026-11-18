
import json
import logging
from datetime import datetime, timezone
from pathlib import Path


class AuditLogger:
    """Журнал аудита событий информационной безопасности."""

    def __init__(self, log_file="audit_log.jsonl"):
        self.log_file = Path(log_file)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log_event(self, event_type, severity, source, details):
        """Запись события безопасности в журнал."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "severity": severity,
            "source": source,
            "details": details
        }

        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

        logging.info("Событие аудита: %s", event_type)
        return event

    def read_events(self):
        """Чтение записей журнала аудита."""
        if not self.log_file.exists():
            return []

        with self.log_file.open("r", encoding="utf-8") as file:
            return [json.loads(line) for line in file if line.strip()]


def main():
    audit = AuditLogger()

    audit.log_event(
        event_type="POTENTIAL_DDOS",
        severity="HIGH",
        source="192.168.1.10",
        details="Превышение порога 1000 пакетов в секунду"
    )

    audit.log_event(
        event_type="BLOCKED_PORT",
        severity="MEDIUM",
        source="192.168.1.25",
        details="Обнаружено обращение к заблокированному порту 23"
    )

    print("\nЖУРНАЛ АУДИТА")
    for event in audit.read_events():
        print(json.dumps(event, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
