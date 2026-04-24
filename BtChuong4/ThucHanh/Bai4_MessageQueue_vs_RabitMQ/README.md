# Bai4: Message Queue vs RabbitMQ

This lab demonstrates a simple message queue system using RabbitMQ.

## Components

- **producer.py**: Sends messages to the RabbitMQ queue.
- **consumer.py**: Receives messages from the RabbitMQ queue.
- **Dockerfile**: Builds the Python application container.
- **docker-compose.yml**: Orchestrates RabbitMQ, producer, and consumer services.

## Running the Lab

1. Ensure Docker and Docker Compose are installed.

2. Run the services:
   ```bash
   docker-compose up
   ```

3. The producer will send 10 messages, and the consumer will receive them.

4. Access RabbitMQ management UI at http://localhost:15672 (username: admin, password: admin).

## Stopping

```bash
docker-compose down
```
