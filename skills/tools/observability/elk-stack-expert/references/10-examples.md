# Examples

## 10.1 Logstash Pipeline

```conf
input {
  file {
    path => "/var/log/syslog"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{HOSTNAME:host} %{DATA:program}: %{GREEDYDATA:log}" }
  }
  date {
    match => [ "timestamp", "MMM dd HH:mm:ss" ]
  }
  mutate {
    remove_field => [ "message" ]
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "syslog-%{+YYYY.MM.dd}"
  }
}
```

## 10.2 Elasticsearch Query

```json
GET /logs-2024-01/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "error" } }
      ],
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-1h"
          }
        }
      }
    }
  },
  "size": 100
}
```

## 10.3 Kibana Visualization (JSON)

```json
{
  "title": "Error Rate",
  "type": "line",
  "params": {
    "xAxisField": "@timestamp",
    "yAxisField": "count"
  },
  "aggs": [
    {
      "type": "count",
      "field": "message"
    }
  ]
}
```

## 10.4 Filebeat Configuration

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log
  fields:
    service: myapp

output.logstash:
  hosts: ["logstash:5044"]

processors:
- add_host_metadata:
    when.not.contains.tags: forwarded
```