# Scenario Examples

## 9.1 Custom Dashboard

**User:** "How do I create a dashboard for my application?"

**Datadog Expert:**
> **Dashboard Setup:**
>
> ```json
> {
>   "title": "MyApp Overview",
>   "widgets": [
>     {
>       "type": "timeseries",
>       "title": "Request Rate",
>       "definition": {
>         "requests": {
>           "q": "sum:app.requests{*}.as_rate()",
>           "style": { "line_width": "normal" }
>         }
>       }
>     },
>     {
>       "type": "query_value",
>       "title": "Error Rate %",
>       "definition": {
>         "requests": {
>           "q": "sum:app.errors{*}.as_count() / sum:app.requests{*}.as_count() * 100",
>           "style": { "unit": "percent" }
>         }
>       }
>     },
>     {
>       "type": "top_list",
>       "title": "Top Endpoints",
>       "definition": {
>         "requests": {
>           "q": "top(5, sum:app.requests{*} by {endpoint})"
>         }
>       }
>     }
>   ]
> }
> ```

## 9.2 APM Service Map

**User:** "How do I visualize service dependencies?"

**Datadog Expert:**
> **Service Map Setup:**
>
> The Service Map automatically shows:
> - Service connections
> - Average latency
> - Error rates
> - Request volume
>
> To enhance visibility:
>
> ```python
> # Add custom service tags
> from ddtrace import config
> config.service = "payment-service"
> config.env = "production"
> config.version = "1.2.3"
>
> # Link services via HTTP headers
> @tracer.wrap("http.call")
> def call_downstream(url, headers=None):
>     headers = headers or {}
>     headers["x-trace-id"] = str(tracer.current_span().trace_id)
>     # Make HTTP request
> ```

## 9.3 Alerting Setup

**User:** "How do I set up SLA alerts?"

**Datadog Expert:**
> **SLO Monitoring:**
>
> ```yaml
> # SLO Definition
> name: API Availability
> type: metric
> query:
>   numerator: >
>     sum(last_5m):sum:app.requests{status:2xx}.as_count()
>   denominator: >
>     sum(last_5m):sum:app.requests{*}.as_count()
> target: 99.9
> 
> # Alert when SLO at risk
> alert: SLO_At_Risk_API_Availability
> query: >
>   current_slo("slo_api_availability") < 99.9
> message: |
>   API SLO is at risk of breaching 99.9%
>   Current: {{ slo_value }}%
>   Target: 99.9%
> ```

## 9.4 Log Analysis

**User:** "How do I search logs efficiently?"

**Datadog Expert:**
> **Log Queries:**
>
> ```logql
> # All errors
> status:error
> 
> # Specific service
> service:payment AND status:error
> 
> # Time range
> @duration:>1s AND service:api
> 
> # Complex query
> service:web AND status:error AND @error.message:*database*
> 
> # Aggregate logs
> stats by @user.id count() > 10
> ```
