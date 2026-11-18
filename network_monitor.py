
from datetime import datetime, timedelta
from collections import Counter
import random


class NetworkTrafficAnalyzer:
    """Система мониторинга сетевого трафика предприятия."""

    def __init__(self, company_name="ТехноПрофи", ddos_threshold=1000):
        self.company_name = company_name
        self.ddos_threshold = ddos_threshold
        self.traffic_log = []
        self.alerts = []

    def simulate_traffic(self):
        """Генерация учебных данных сетевого трафика."""
        random.seed(42)
        start = datetime.now().replace(microsecond=0)

        for second in range(60):
            timestamp = start + timedelta(seconds=second)

            # Обычная нагрузка: 20–80 пакетов в секунду
            packet_count = random.randint(20, 80)

            # Имитация аномального всплеска на 30-й секунде
            if second == 30:
                packet_count = 1500

            for _ in range(packet_count):
                self.traffic_log.append({
                    "timestamp": timestamp,
                    "source_ip": f"192.168.1.{random.randint(1, 200)}",
                    "destination_ip": "192.168.1.10",
                    "protocol": random.choice(["HTTP", "HTTPS", "DNS"])
                })

        print(f"Предприятие: {self.company_name}")
        print(f"Сгенерировано пакетов: {len(self.traffic_log)}")

    def detect_ddos(self):
        """Обнаружение возможных DDoS-атак по числу пакетов в секунду."""
        print("\nАНАЛИЗ DDOS-АТАК")

        packets_per_second = Counter(
            packet["timestamp"] for packet in self.traffic_log
        )

        for timestamp, count in sorted(packets_per_second.items()):
            if count > self.ddos_threshold:
                alert = {
                    "timestamp": timestamp.isoformat(),
                    "type": "POTENTIAL_DDOS",
                    "severity": "HIGH",
                    "packets_per_second": count,
                    "details": "Превышен порог сетевой активности"
                }

                self.alerts.append(alert)

                print(
                    f"ВНИМАНИЕ! Возможная DDoS-атака: "
                    f"{count} пакетов/сек., время: {timestamp}"
                )

        if not self.alerts:
            print("Признаков DDoS-атак не обнаружено.")

        return self.alerts


def main():
    analyzer = NetworkTrafficAnalyzer()
    analyzer.simulate_traffic()
    analyzer.detect_ddos()


if __name__ == "__main__":
    main()
