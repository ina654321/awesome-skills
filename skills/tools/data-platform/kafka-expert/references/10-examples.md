# Examples

## 10.1 Producer Configuration

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");
props.put("retries", 3);
props.put("batch.size", 16384);
props.put("linger.ms", 10);
props.put("compression.type", "snappy");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

ProducerRecord<String, String> record = new ProducerRecord<>("my-topic", "key", "value");
producer.send(record);
producer.flush();
producer.close();
```

## 10.2 Consumer Configuration

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-consumer-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("auto.offset.reset", "earliest");
props.put("enable.auto.commit", "true");
props.put("auto.commit.interval.ms", "5000");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("my-topic"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(100);
    for (ConsumerRecord<String, String> record : records) {
        System.out.println(record.value());
    }
}
```

## 10.3 Create Topic

```bash
# Create topic with 3 partitions and 2 replicas
kafka-topics.sh --create \
  --topic my-topic \
  --partitions 3 \
  --replication-factor 2 \
  --bootstrap-server localhost:9092

# With config
kafka-topics.sh --create \
  --topic my-topic \
  --partitions 6 \
  --replication-factor 3 \
  --config retention.ms=86400000 \
  --bootstrap-server localhost:9092
```

## 10.4 Kafka Streams Word Count

```java
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.serialization.*;

Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "wordcount-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

StreamsBuilder builder = new StreamsBuilder();
KStream<String, String> textLines = builder.stream("text-lines");
KTable<String, Long> wordCounts = textLines
    .flatMapValues(textLine -> Arrays.asList(textLine.toLowerCase().split("\\W+")))
    .groupBy((key, word) -> word)
    .count(Materialized.as("counts"));

wordCounts.toStream().to("word-counts-output");

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

## 10.5 Kafka Connect Source (File)

```json
{
  "name": "file-source",
  "config": {
    "connector.class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "tasks.max": "1",
    "file": "/tmp/test.txt",
    "topic": "file-topic"
  }
}
```

## 10.6 Kafka Connect Sink (JDBC)

```json
{
  "name": "jdbc-sink",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "topics": "orders",
    "connection.url": "jdbc:postgresql://localhost:5432/mydb",
    "connection.user": "user",
    "connection.password": "pass",
    "auto.create": "true",
    "auto.evolve": "true",
    "insert.mode": "upsert",
    "pk.fields": "order_id"
  }
}
```

## 10.7 Admin Client - List Topics

```java
import org.apache.kafka.clients.admin.*;

Properties props = new Properties();
props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

try (AdminClient admin = AdminClient.create(props)) {
    ListTopicsResult result = admin.listTopics();
    Set<String> names = result.names().get();
    System.out.println("Topics: " + names);
}
```

## 10.8 Exactly-Once Semantics

```java
// Producer
props.put("enable.idempotence", "true");
props.put("transactional.id", "my-transactional-id");
props.put("acks", "all");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();
producer.beginTransaction();
producer.send(new ProducerRecord<>("topic1", "key", "value1"));
producer.send(new ProducerRecord<>("topic2", "key", "value2"));
producer.commitTransaction();

// Consumer
props.put("isolation.level", "read_committed");
```

## 10.9 Schema Registry Producer

```java
import io.confluent.kafka.serializers.*;

Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(SerializerConfig.KEY_SERIALIZATION_CLASS_CONFIG, StringSerializer.class);
props.put(SerializerConfig.VALUE_SERIALIZATION_CLASS_CONFIG, KafkaAvroSerializer.class);
props.put("schema.registry.url", "http://localhost:8081");

KafkaProducer<String, User> producer = new KafkaProducer<>(props);
User user = User.newBuilder().setName("John").build();
producer.send(new ProducerRecord<>("user-topic", user.getId().toString(), user));
```

## 10.10 Monitoring with JMX

```bash
# Enable JMX
export JMX_PORT=9999

# View MBeans
jconsole localhost:9999

# Key metrics
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
kafka.consumer:type=ConsumerLagMetrics,client-id=client-id
kafka.producer:type=ProducerMetrics,client-id=client-id
```