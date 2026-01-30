import json
from aiokafka import AIOKafkaConsumer
import asyncio
import os
from datetime import datetime


class KafkaConsumer:
    def __init__(self):
        self.consumer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.running = False

    async def start(self):
        """Initialize and start the Kafka consumer"""
        self.consumer = AIOKafkaConsumer(
            "task-events",
            "reminder-events",
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        await self.consumer.start()
        self.running = True
        print("Kafka consumer started")

    async def stop(self):
        """Stop the Kafka consumer"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()

    async def consume_events(self):
        """Consume events from Kafka topics"""
        if not self.consumer:
            return

        try:
            async for msg in self.consumer:
                print(f"Received message: {msg.value} from topic: {msg.topic}")

                # Process different types of events
                if msg.topic == "task-events":
                    await self.process_task_event(msg.value)
                elif msg.topic == "reminder-events":
                    await self.process_reminder_event(msg.value)

        except Exception as e:
            print(f"Error consuming messages: {e}")

    async def process_task_event(self, event_data):
        """Process task-related events"""
        event_type = event_data.get("event_type")
        task_data = event_data.get("data", {})

        print(f"Processing task event: {event_type}")

        # Here you could trigger notifications, update other services, etc.
        if event_type == "task_created":
            print(f"Task created: {task_data.get('title')}")
        elif event_type == "task_updated":
            print(f"Task updated: {task_data.get('id')}")
        elif event_type == "task_completed":
            print(f"Task completed: {task_data.get('id')}")

    async def process_reminder_event(self, event_data):
        """Process reminder events"""
        task_id = event_data.get("task_id")
        user_id = event_data.get("user_id")
        due_date_str = event_data.get("due_date")
        message = event_data.get("message")

        print(f"Processing reminder for task {task_id}, user {user_id}")

        # Here you could send email notifications, push notifications, etc.
        # For now, just print the reminder
        print(f"REMINDER: {message} - Task ID: {task_id}, Due: {due_date_str}")


# Global consumer instance
kafka_consumer = KafkaConsumer()