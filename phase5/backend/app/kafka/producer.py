import json
from typing import Dict, Any
from aiokafka import AIOKafkaProducer
import asyncio
import os


class KafkaProducer:
    def __init__(self):
        self.producer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    async def start(self):
        """Initialize the Kafka producer"""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

    async def stop(self):
        """Stop the Kafka producer"""
        if self.producer:
            await self.producer.stop()

    async def send_task_event(self, event_type: str, task_data: Dict[Any, Any]):
        """Send a task-related event to Kafka"""
        event = {
            "event_type": event_type,
            "timestamp": asyncio.get_event_loop().time(),
            "data": task_data
        }

        await self.producer.send_and_wait("task-events", event)
        print(f"Sent {event_type} event to Kafka: {event}")

    async def send_reminder_event(self, task_id: int, user_id: int, due_date: str, message: str):
        """Send a reminder event to Kafka"""
        event = {
            "event_type": "reminder",
            "task_id": task_id,
            "user_id": user_id,
            "due_date": due_date,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        }

        await self.producer.send_and_wait("reminder-events", event)
        print(f"Sent reminder event to Kafka: {event}")


# Global producer instance
kafka_producer = KafkaProducer()