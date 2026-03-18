## 9. Quality Verification Checklist

When you've completed prompt engineering work, verify against this checklist:

**Prompt Design Quality**:
- [ ] Success criteria defined before writing the first prompt (measurable, not vague)
- [ ] At least 2 prompt variations created and A/B tested on representative examples
- [ ] Token count estimated for production load (cost × volume = monthly cost)
- [ ] Model-specific quirks documented (e.g., Claude prefers XML tags, GPT-4 prefers JSON)
- [ ] Adversarial inputs tested (prompt injection, edge cases, empty input)

**Few-Shot Examples Quality**:
- [ ] Examples cover the full output distribution (not just easy cases)
- [ ] Minimum 5 examples; 20+ for production-critical tasks
- [ ] Examples are diverse (different inputs, edge cases, failure modes)
- [ ] Label quality verified by domain expert, not just prompt engineer

**Evaluation Framework**:
- [ ] Evaluation set is held-out (not used for prompt optimization)
- [ ] LLM-as-judge criteria calibrated against human ratings (Cohen's κ > 0.7)
- [ ] Regression test suite covers all previously-observed failure modes
- [ ] Metrics dashboard running for production monitoring

**RAG Pipeline (if applicable)**:
- [ ] Retrieval precision@K measured (not just recall)
- [ ] Chunk size validated empirically on target document type
- [ ] Hallucination rate measured with and without retrieval
- [ ] Context window utilization tracked (not just filling to max)

**Production Readiness**:
- [ ] Latency measured end-to-end at expected concurrency
- [ ] Fallback behavior defined for model failures or timeouts
- [ ] Output schema validated programmatically (not trusted as valid JSON/structured output)
- [ ] Cost estimate provided for expected monthly volume

