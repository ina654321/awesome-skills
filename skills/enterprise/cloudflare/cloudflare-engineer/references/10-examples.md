# Examples

## 10.1 DNS Record Management

```bash
# Create A record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"blog","content":"192.0.2.1","ttl":3600}'

# Create CNAME record (proxied)
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"www","content":"example.com","proxied":true}'

# Update record
curl -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"api","content":"192.0.2.2","ttl":300}'
```

## 10.2 Page Rules Configuration

```json
{
  "rules": [
    {
      "id": "rule-id",
      "actions": {
        "cache_level": "cache_everything",
        "edge_cache_ttl": 604800,
        "browser_cache_ttl": 604800,
        "always_use_https": true,
        "automatic_https_rewrites": "on"
      },
      "matchers": {
        "url": "example.com/static/*"
      }
    },
    {
      "id": "rule-id-2",
      "actions": {
        "disable_security": true
      },
      "matchers": {
        "url": "example.com/api/*"
      }
    }
  ]
}
```

## 10.3 WAF Rule Configuration

```bash
# Create firewall rule - block IP
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "filter": {"expression": "ip.src eq 192.0.2.1"},
    "action": "block"
  }'

# Rate limiting rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "filter": {"expression": "http.request.uri contains \"/api/\" and http.request.method eq POST"},
    "action": "rate_limit",
    "action_parameters": {"rate_limit": {"period": 60, "requests_per_period": 10}}
  }'
```

## 10.4 Workers Script

```javascript
// worker.js
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Add custom header
    const response = await fetch(request);
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('X-Custom-Edge', 'true');
    newResponse.headers.set('CF-Cache-Status', response.headers.get('CF-Cache-Status'));
    
    return newResponse;
  },
  
  async scheduled(event, env, ctx) {
    // Cron trigger handler
    console.log('Scheduled task running');
    
    // Fetch and process data
    await fetch('https://api.example.com/sync', { method: 'POST' });
  }
};
```

```javascript
// worker.js - with KV
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/get') {
      const value = await env.MY_KV.get('mykey');
      return new Response(value);
    }
    
    if (url.pathname === '/set') {
      await env.MY_KV.put('mykey', 'myvalue', { expirationTtl: 3600 });
      return new Response('Stored');
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

## 10.5 Access Policy (Zero Trust)

```bash
# Create Access application
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/access/apps" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name":"Internal Dashboard",
    "domain":"internal.example.com",
    "session_duration": "24h",
    "auto_redirect_to_identity": true
  }'

# Add Access policy
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/access/apps/$APP_ID/policies" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name":"Engineering",
    "decision":"allow",
    "include":[{"group":{"id":"group-id"}}],
    "require":[{"email":{"domain":"example.com"}}]
  }'
```

## 10.6 Load Balancer Setup

```bash
# Create health check
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/load_balancers/healthchecks" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name":"web-health",
    "type":"http",
    "url":"https://example.com/health",
    "interval":60,
    "timeout":5,
    "retries":3
  }'

# Create pool
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/load_balancers/pools" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name":"web-pool",
    "origins":[{"address":"192.0.2.1","enabled":true}],
    "health_check":"web-health"
  }'

# Create load balancer
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/load_balancers" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name":"web-lb",
    "fallback_pool":"web-pool-fallback",
    "default_pool_ids":["web-pool-id"],
    "proxied":true,
    "description":"Main load balancer"
  }'
```

## 10.7 Cache Purge

```bash
# Purge by URL
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://example.com/index.html"]}'

# Purge by tag
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"tags":["product-123","category-electronics"]}'

# Purge everything
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```