## 10. Common Pitfalls & Anti-Patterns

### High Severity

**Anti-Pattern 1: No Evaluation Before Deploy

```
BAD:  "The RAG system feels good in testing, let's ship it."

GOOD: Build an eval set of 50+ QA pairs before writing a single line of prod code.
      Establish Faithfulness, Answer Relevancy baselines.
      Every code change must be measured against the eval set.
      "Feels good" is not a metric.
```

**Anti-Pattern 2: Flat Retrieval (k=3 Dense Only)

```
BAD:  retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
      # Misses 30-40% of relevant context; no precision control

GOOD: Use hybrid retrieval (BM25 + dense) with k=20,
      then rerank to top 5 with cross-encoder.
      Result: 20-30% improvement in context_recall;
              10-15% improvement in context_precision.
```

### Medium Severity

**Anti-Pattern 3: Synchronous Chain Without Fallback

```
BAD:  response = openai.chat(model="gpt-4o", ...)  # No timeout, no fallback
      # Single provider failure → full outage

GOOD: Use litellm or LangChain's LLMRouter with:
      Primary: OpenAI GPT-4o (timeout=30s)
      Fallback: Anthropic Claude 3.5 Sonnet
      Last resort: Return cached response
```

**Anti-Pattern 4: Ignoring Streaming for UX

```
BAD:  response = llm.invoke(prompt)  # Wait 5-10s, then dump full response
      User thinks the system is broken after 3s.

GOOD: Use async streaming:
      async for chunk in llm.astream(prompt):
          yield chunk
      Users see the first token in <500ms regardless of total generation time.
      Perceived latency drops 60-80%.
```

