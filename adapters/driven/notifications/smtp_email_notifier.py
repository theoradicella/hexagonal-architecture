import smtplib
from email.mime.text import MIMEText

from domain.entities.order import Order
from domain.entities.vendor import Vendor


class SmtpEmailNotifier:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def _send(self, to: str, subject: str, body: str) -> None:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = to

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)

    async def send_order_confirmation(self, order: Order, vendor: Vendor) -> None:
        self._send(
            to=vendor.contact_email,
            subject=f"Order #{order.id} confirmed",
            body=f"New order #{order.id} received. Total: {order.total_amount}.",
        )

    async def send_status_update(self, order: Order, vendor: Vendor) -> None:
        self._send(
            to=vendor.contact_email,
            subject=f"Order #{order.id} status update",
            body=f"Order #{order.id} is now {order.status.value}.",
        )
