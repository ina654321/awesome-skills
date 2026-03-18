## 8. Standard Workflow

### Phase 1: RAG System Build

**Objective**: Deliver a production-ready RAG pipeline with measurable quality baseline


| Step | Activity | Done Criteria | Fail Criteria |
|------|----------|--------------|---------------|
| 1 | Build evaluation set: 50+ QA pairs from target documents | Eval set covers 5+ document types and query categories | < 30 QA pairs or only easy questions |
| 2 | Baseline: naive chunking + dense retrieval + GPT-4o | Faithfulness > 0.7, Answer Relevancy > 0.7 | Either metric < 0.6 → identify bottleneck first |
| 3 | Optimize retrieval: hybrid search (BM25 + dense) | Context Recall improves by ≥ 10% over baseline | No improvement → check embedding model mismatch |
| 4 | Add reranking (cross-encoder or Cohere Rerank) | Context Precision improves by ≥ 10% | No improvement → review chunk granularity |
| 5 | Optimize generation prompt: add citation requirement | Faithfulness improves by ≥ 5% | Hallucination rate still > 15% → consider smaller model |
| 6 | Load test at 2× expected QPS | P95 latency < 2s | P95 > 3s → profile and optimize each stage |

### Phase 2: Production Optimization

**Objective**: Achieve cost target and observability coverage


| Step | Activity | Done Criteria | Fail Criteria |
|------|----------|--------------|---------------|
| 1 | Implement semantic caching (Redis + similarity threshold 0.95) | Cache hit rate > 30% for repeated query patterns | < 10% → queries too diverse or threshold too strict |
| 2 | Model tiering: route simple queries to smaller model | Cost reduction ≥ 25% with quality loss < 5% | Quality loss > 10% → refine routing logic |
| 3 | Deploy tracing: every LLM call traced to LangSmith/Langfuse | 100% of production calls traced | Sampling < 100% → full tracing first, sample later |
| 4 | Add prompt injection detection on user inputs | Zero injection bypass in red-team test of 100 attempts | Any bypass → harden detection layer |

