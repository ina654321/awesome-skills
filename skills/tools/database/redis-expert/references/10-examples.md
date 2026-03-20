# Examples

## 10.1 Data Structure Patterns

### Cache-Aside Pattern

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id):
    # Check cache
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    user = db.fetch("SELECT * FROM users WHERE id = ?", user_id)
    
    # Store in cache with 1-hour TTL
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

def update_user(user_id, data):
    # Update database
    db.execute("UPDATE users SET ... WHERE id = ?", user_id)
    
    # Invalidate cache
    r.delete(f"user:{user_id}")
```

### Distributed Lock

```python
import time
import uuid

def acquire_lock(r, lock_name, timeout=10):
    lock_key = f"lock:{lock_name}"
    token = str(uuid.uuid4())
    
    if r.set(lock_key, token, nx=True, ex=timeout):
        return token
    return None

def release_lock(r, lock_name, token):
    lock_key = f"lock:{lock_name}"
    
    # Lua script for atomic check-and-delete
    script = """
    if redis.call("GET", KEYS[1]) == ARGV[1] then
        return redis.call("DEL", KEYS[1])
    else
        return 0
    end
    """
    r.eval(script, 1, lock_key, token)

def with_lock(r, lock_name, func, timeout=10):
    token = acquire_lock(r, lock_name, timeout)
    if not token:
        raise Exception("Could not acquire lock")
    try:
        return func()
    finally:
        release_lock(r, lock_name, token)
```

### Rate Limiting

```python
def is_rate_limited(r, client_id, limit=100, window=60):
    key = f"ratelimit:{client_id}"
    
    # Sliding window counter
    now = time.time()
    window_start = now - window
    
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)
    pipe.zcard(key)
    pipe.zadd(key, {str(now): now})
    pipe.expire(key, window)
    results = pipe.execute()
    
    return results[1] >= limit
```

### Leaderboard

```python
def update_leaderboard(r, player_id, score):
    r.zadd("leaderboard", {player_id: score})

def get_top_players(r, count=10):
    return r.zrevrange("leaderboard", 0, count - 1, withscores=True)

def get_player_rank(r, player_id):
    rank = r.zrevrank("leaderboard", player_id)
    return rank + 1 if rank is not None else None

def get_player_score(r, player_id):
    return r.zscore("leaderboard", player_id)

def increment_score(r, player_id, delta):
    return r.zincrby("leaderboard", delta, player_id)
```

## 10.2 Queue Patterns

### Work Queue

```python
# Producer
def enqueue_job(r, job_data):
    r.lpush("jobs:queue", json.dumps(job_data))

# Worker
def process_jobs(r):
    while True:
        _, job = r.brpop("jobs:queue", timeout=5)
        if job:
            data = json.loads(job)
            process(data)
```

### Priority Queue

```python
def enqueue_priority(r, priority, data):
    # Lower score = higher priority
    r.zadd("priority:queue", {json.dumps(data): priority})

def dequeue_priority(r):
    result = r.zpopmin("priority:queue", 1)
    if result:
        _, data = result[0]
        return json.loads(data)
    return None
```

### Delayed Job

```python
from datetime import datetime, timedelta

def schedule_job(r, delay_seconds, job_data):
    execute_at = datetime.now() + timedelta(seconds=delay_seconds)
    timestamp = execute_at.timestamp()
    r.zadd("delayed:queue", {json.dumps(job_data): timestamp})

def process_delayed_jobs(r):
    now = datetime.now().timestamp()
    jobs = r.zrangebyscore("delayed:queue", 0, now)
    
    for job_json in jobs:
        if r.zrem("delayed:queue", job_json):
            job = json.loads(job_json)
            process(job)
```

## 10.3 Pub/Sub Patterns

```python
# Publisher
def publish_event(r, channel, event_data):
    r.publish(channel, json.dumps(event_data))

# Subscriber
def subscribe_to_channel(r, channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            handle_event(data)

# Pattern subscription
pubsub = r.pubsub()
pubsub.psubscribe('events:*', 'logs:*')
```

## 10.4 Stream Patterns

```python
# Add to stream
def add_to_stream(r, stream_name, data):
    r.xadd(stream_name, data)

# Consumer group
def create_group(r, stream, group):
    try:
        r.xgroup_create(stream, group, id='0')
    except redis.exceptions.ResponseError:
        pass  # Group exists

def consume_messages(r, stream, group, consumer):
    messages = r.xreadgroup(group, consumer, {stream: '>'}, count=10)
    
    for stream_name, entries in messages:
        for msg_id, data in entries:
            process(data)
            r.xack(stream_name, group, msg_id)

# Fan-out to multiple consumers
def process_with_multiple_consumers(r, stream, groups, count=10):
    for group in groups:
        create_group(r, stream, group)
    
    streams = {s: '>' for s in [stream] * len(groups)}
    return r.xreadgroup(None, None, streams, count=count)
```

## 10.5 Geo Patterns

```python
# Add locations
def add_location(r, key, longitude, latitude, member):
    r.geoadd(key, (longitude, latitude, member))

# Find nearby
def find_nearby(r, key, longitude, latitude, radius_km, count=10):
    return r.georadius(
        key, longitude, latitude, radius_km,
        unit='km', withdist=True, count=count, sort='ASC'
    )

# Distance between
def get_distance(r, key, member1, member2):
    return r.geodist(key, member1, member2, unit='km')

# Example
add_location(r, "cities", -122.4194, 37.7749, "San Francisco")
add_location(r, "cities", -118.2437, 34.0522, "Los Angeles")
find_nearby(r, "cities", -121.0, 38.0, 500)  # Find cities near Sacramento
```

## 10.6 CLI Commands

```bash
# Basic
redis-cli PING
redis-cli SET key value
redis-cli GET key
redis-cli EXISTS key
redis-cli DEL key

# Strings
redis-cli INCR counter
redis-cli INCRBY counter 10
redis-cli APPEND key "suffix"

# Hashes
redis-cli HSET user:1 name "John" email "john@example.com"
redis-cli HGET user:1 name
redis-cli HGETALL user:1
redis-cli HSCAN user:1 0 MATCH "name*"

# Lists
redis-cli LPUSH mylist "first"
redis-cli RPUSH mylist "last"
redis-cli LRANGE mylist 0 -1

# Sets
redis-cli SADD tags "python" "redis"
redis-cli SMEMBERS tags
redis-cli SISMEMBER tags "python"

# Sorted sets
redis-cli ZADD leaderboard 100 "player1"
redis-cli ZREVRANGE leaderboard 0 9 WITHSCORES

# Scan (avoid KEYS)
redis-cli --scan --pattern "user:*" | head -100
redis-cli --scan --pattern "user:*" | xargs redis-cli TYPE

# Pipeline
redis-cli --pipe <<EOF
SET key1 value1
SET key2 value2
GET key1
EOF

# Monitor
redis-cli MONITOR

# Info
redis-cli INFO
redis-cli INFO memory
redis-cli INFO replication
```

## 10.7 Lua Scripts

```lua
-- Atomic increment with limit
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = tonumber(redis.call('GET', key) or '0')

if current < limit then
    redis.call('INCR', key)
    return current + 1
else
    return -1
end

-- Rate limiter using sliding window
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)

if count < limit then
    redis.call('ZADD', key, now, now)
    redis.call('EXPIRE', key, window)
    return count + 1
else
    return -1
end

-- Execute
redis-cli EVAL "$(cat rate_limiter.lua)" 1 ratelimit:user:1 1000000 60 100
```
