
import json
import os
from urllib import request, error


class SecurityNotifier:
    """Отправка уведомлений об инцидентах безопасности."""

    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    def send_telegram(self, message):
        """Отправка сообщения через Telegram Bot API."""
        if not self.telegram_token or not self.telegram_chat_id:
            print("Telegram: демонстрационный режим")
            print(message)
            return False

        url = (
            f"https://api.telegram.org/bot"
            f"{self.telegram_token}/sendMessage"
        )

        data = json.dumps({
            "chat_id": self.telegram_chat_id,
            "text": message
        }).encode("utf-8")

        req = request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with request.urlopen(req, timeout=10) as response:
                result = json.load(response)
                return result.get("ok", False)
        except (error.URLError, ValueError, TimeoutError) as exc:
            print(f"Ошибка отправки Telegram: {type(exc).__name__}")
            return False

    def send_slack(self, message):
        """Отправка сообщения через Slack Incoming Webhook."""
        if not self.slack_webhook:
            print("Slack: демонстрационный режим")
            print(message)
            return False

        data = json.dumps({"text": message}).encode("utf-8")

        req = request.Request(
            self.slack_webhook,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except (error.URLError, TimeoutError) as exc:
            print(f"Ошибка отправки Slack: {type(exc).__name__}")
            return False

    def notify_security_incident(self, incident):
        """Формирование и отправка уведомления."""
        message = (
            "ОПОВЕЩЕНИЕ О БЕЗОПАСНОСТИ\n"
            f"Тип: {incident['type']}\n"
            f"Уровень: {incident['severity']}\n"
            f"Время: {incident['timestamp']}\n"
            f"Описание: {incident['details']}"
        )

        telegram_sent = self.send_telegram(message)
        slack_sent = self.send_slack(message)

        return {
            "telegram_sent": telegram_sent,
            "slack_sent": slack_sent
        }


if __name__ == "__main__":
    notifier = SecurityNotifier()

    test_incident = {
        "type": "POTENTIAL_DDOS",
        "severity": "HIGH",
        "timestamp": "2026-11-18 12:00:00",
        "details": "Обнаружено 1500 пакетов в секунду"
    }

    notifier.notify_security_incident(test_incident)
