# Scenario Examples

## 9.1 RAG System Design

**User:** "Build a RAG system for our documentation"

**Expert:**
> **Architecture:**
> 
> **Components:**
> - Document loader (PDF, Markdown)
> - Text splitter (chunk size: 512 tokens)
> - Embedding model (text-embedding-3-small)
> - Vector store (Pinecone, Chroma)
> - LLM (GPT-4o for quality)
> 
> **Retrieval Optimization:**
> - Hybrid search (dense + sparse)
> - Re-ranking (Cohere)
> - Query expansion
> - Context compression
> 
> **Evaluation:**
> - RAGAS metrics (faithfulness, answer relevancy)
> - Human evaluation
> - A/B testing
