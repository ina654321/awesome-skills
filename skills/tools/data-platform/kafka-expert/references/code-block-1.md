# python Example

```
from confluent_kafka import Producer
import json

producer = Producer({
    'bootstrap.servers': 'kafka-1:9092,kafka-2:9092,kafka-3:9092',
    'acks': 'all',  # Wait for all in-sync replicas
    'retries': 3,
    'retry.backoff.ms': 100,
    'enable.idempotence': True,  # Exactly-once produce
    'compression.type': 'gzip',  # Compress for throughput
    'batch.size': 16384,  # 16KB batch for efficiency
    'linger.ms': 10,  # Wait up to 10ms for batching
    'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
    'value.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
})


def delivery_report(err, msg):
    """Callback for delivery confirmation."""
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")


producer.produce(
    'orders.events',
    key='user-123',
    value=json.dumps({'order_id': 1, 'total': 99.99}),
    callback=delivery_report,
)
producer.flush()
```
