## 7. Standards & Reference

### RAG Quality Metrics

| Metric / 指标 | Formula / 公式 | Target / 目标 | Tool
|--------------|--------------|--------------|------------|
| **Faithfulness** | (factual claims in context)
| **Answer Relevancy** | semantic similarity(answer, question) | > 0.80 | Ragas |
| **Context Precision** | (relevant retrieved chunks)
| **Context Recall** | (relevant chunks retrieved)
| **Retrieval Latency** | P95 time for retrieval stage | < 200ms | LangSmith |
| **End-to-End Latency** | P95 total response time | < 3s (streaming) | APM |

### Chunking Decision Matrix

| Document Type / 文档类型 | Chunk Size / 大小 | Overlap / 重叠 | Strategy
|------------------------|-----------------|--------------|----------------|
| Technical docs | 512 tokens | 10% | Fixed-size + sentence boundary |
| Legal
| Code files | By function/class | 0% | AST-aware chunking |
| Conversations | By turn | 5% | Fixed-size |
| Tables

