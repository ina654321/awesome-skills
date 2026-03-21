# code Example

```
Index Lifecycle: hot → warm → cold → delete (or searchable_snapshot)

┌─────────────────────────────────────────────────────────────┐
│  ILM Policy for Application Logs                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  hot (0-7 days):                                             │
│    - Primary/replica: 1 shard, 1 replica                     │
│    - Refresh interval: 1s                                    │
│    - Roll over when: size > 50GB OR docs > 20M              │
│                                                              │
│  warm (7-30 days):                                           │
│    - Shrink to 1 primary shard                              │
│    - Force merge to 1 segment                                │
│    - Move to warm nodes (HDD)                                │
│                                                              │
│  cold (30-90 days):                                          │
│    - Move to cold nodes (larger HDDs)                        │
│    - Reduce replicas to 0                                    │
│    - Optionally freeze                                       │
│                                                              │
│  delete (90+ days):                                          │
│    - Delete index                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
