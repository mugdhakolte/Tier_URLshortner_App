import json
from typing import Dict, Any, Optional

import pika
from django.conf import settings


class ArticlePublisher:
    """Publishes article details to a RabbitMQ exchange."""

    def __init__(
        self,
        url: Optional[str] = None,
        exchange: Optional[str] = None,
        exchange_type: Optional[str] = None,
        routing_key: Optional[str] = None,
    ) -> None:
        self.url = url or settings.PUBSUB_URL
        self.exchange = exchange or settings.PUBSUB_EXCHANGE
        self.exchange_type = exchange_type or settings.PUBSUB_EXCHANGE_TYPE
        self.routing_key = routing_key or settings.PUBSUB_ROUTING_KEY

    def publish(self, article: Dict[str, Any]) -> None:
        """Publish the given article dictionary as JSON."""
        connection_params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(connection_params)
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.exchange,
                exchange_type=self.exchange_type,
                durable=True,
            )
            payload = json.dumps(article).encode("utf-8")
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=payload,
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2,
                ),
            )
        finally:
            try:
                connection.close()
            except Exception:
                pass