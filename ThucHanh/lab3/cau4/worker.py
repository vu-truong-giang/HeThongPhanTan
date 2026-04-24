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

channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    print("[x] Received:", body.decode())

    time.sleep(5)

    print("[x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='task_queue',
    on_message_callback=callback,
    auto_ack=False
)

print(" [*] Waiting for messages...")
channel.start_consuming()