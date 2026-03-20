# Examples

## 10.1 Mapping Design

### Text with Keyword Fallback

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": { 
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "category": { "type": "keyword" },
      "price": { "type": "float" },
      "tags": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

### Nested Object

```json
PUT /orders
{
  "mappings": {
    "properties": {
      "order_id": { "type": "keyword" },
      "items": {
        "type": "nested",
        "properties": {
          "product_id": { "type": "keyword" },
          "quantity": { "type": "integer" },
          "price": { "type": "float" }
        }
      }
    }
  }
}
```

## 10.2 Query DSL Examples

### Boolean Query

```json
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "laptop" } }
      ],
      "filter": [
        { "term": { "category": "electronics" } },
        { "range": { "price": { "gte": 500, "lte": 2000 } } }
      ],
      "should": [
        { "term": { "in_stock": true } }
      ],
      "must_not": [
        { "term": { "brand": "Generic" } }
      ]
    }
  }
}
```

### Multi-Match Query

```json
GET /articles/_search
{
  "query": {
    "multi_match": {
      "query": "elasticsearch tutorial",
      "fields": ["title^3", "content", "tags^2"],
      "type": "best_fields",
      "fuzziness": "AUTO"
    }
  }
}
```

### Nested Query

```json
GET /orders/_search
{
  "query": {
    "nested": {
      "path": "items",
      "query": {
        "bool": {
          "must": [
            { "term": { "items.product_id": "PROD-123" } },
            { "range": { "items.quantity": { "gte": 2 } } }
          ]
        }
      }
    }
  }
}
```

## 10.3 Aggregations

### Terms Aggregation

```json
GET /sales/_search
{
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": { "field": "category", "size": 20 },
      "aggs": {
        "total_revenue": { "sum": { "field": "amount" } },
        "avg_order": { "avg": { "field": "amount" } }
      }
    }
  }
}
```

### Date Histogram with Stats

```json
GET /logs/_search
{
  "size": 0,
  "aggs": {
    "requests_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "latency_stats": { "stats": { "field": "latency_ms" } },
        "p95_latency": {
          "percentiles": { "field": "latency_ms", "percents": [50, 95, 99] }
        }
      }
    }
  }
}
```

### Filtered Aggregation

```json
GET /sales/_search
{
  "size": 0,
  "aggs": {
    "filtered_sales": {
      "filter": { "range": { "date": { "gte": "2024-01-01" } } },
      "aggs": {
        "by_region": {
          "terms": { "field": "region" },
          "aggs": {
            "revenue": { "sum": { "field": "amount" } }
          }
        }
      }
    }
  }
}
```

## 10.4 Index Lifecycle Management

```json
PUT /_ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_age": "7d",
            "max_primary_shard_size": "50gb"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## 10.5 Reindexing

```json
POST /_reindex
{
  "source": {
    "index": "old-index",
    "size": 5000,
    "query": {
      "range": { "created_at": { "gte": "2024-01-01" } }
    },
    "sort": { "created_at": "asc" }
  },
  "dest": {
    "index": "new-index"
  },
  "script": {
    "source": "ctx._source.price *= 1.1",
    "lang": "painless"
  }
}
```

## 10.6 Search After Pagination

```json
GET /products/_search
{
  "size": 100,
  "sort": [
    { "price": "asc" },
    { "_id": "asc" }
  ],
  "query": { "match_all": {} }
}
```

Then use last document's sort values for next page:

```json
GET /products/_search
{
  "size": 100,
  "search_after": [100, "doc_id_abc"],
  "sort": [
    { "price": "asc" },
    { "_id": "asc" }
  ],
  "query": { "match_all": {} }
}
```
