import pika
import time

max_retries = 10
retry_delay = 3

for attempt in range(max_retries):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq', connection_attempts=3, retry_delay=2)
        )
        channel = connection.channel()
        print("[✓] Connected to RabbitMQ")
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[✗] Connection failed (attempt {attempt + 1}/{max_retries}): {e}")
        if attempt < max_retries - 1:
            print(f"[⏳] Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("[✗] Failed to connect after all retries")
            raise

channel.queue_declare(queue='task_queue', durable=True)

for i in range(10):
    message = f"Task {i}"

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print("[x] Sent", message)
    time.sleep(1)

connection.close()