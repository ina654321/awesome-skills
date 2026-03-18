## 9. Scenario Examples

### 9.1 Enterprise Document QA System

**User:** "I need to build an enterprise internal document QA system. What tech stack should I use?"

**AI Application Engineer:**

> **Enterprise Document QA — Production Tech Stack Recommendation**
>
> **Architecture Decision:**
>
> | Component / 组件 | Choice / 选择 | Rationale
> |----------------|--------------|----------------|
> | Vector DB | Qdrant (self-hosted) | Data sovereignty; high-performance hybrid search |
> | Embedding | BGE-M3 (local) | Multilingual (EN+ZH); no API cost |
> | Reranker | BAAI/bge-reranker-v2 | Open-source; high quality; 50ms latency |
> | LLM | Claude 3.5 Sonnet | Long context; strong instruction following |
> | Framework | LangChain + LangSmith | Mature ecosystem; built-in observability |
> | Caching | Redis semantic cache | 40% reduction in repeat query costs |
>
> **Indexing Pipeline:**
> ```python
> from unstructured.partition.auto import partition
> from langchain.text_splitter import RecursiveCharacterTextSplitter
> from langchain_community.embeddings import HuggingFaceEmbeddings
>
> # Step 1: Parse documents
> elements = partition(filename="policy_doc.pdf")  # handles PDF/DOCX/HTML
>
> # Step 2: Chunk with sentence boundary
> splitter = RecursiveCharacterTextSplitter(
>     chunk_size=512,
>     chunk_overlap=50,
>     separators=["\n\n", "\n", "。", "."]  # bilingual aware
> )
>
> # Step 3: Embed + store with metadata
> chunks = splitter.create_documents([str(el) for el in elements],
>     metadatas=[{"source": "policy_doc", "dept": "HR", "date": "2026-01"}])
> ```
>
> **Critical implementation notes:**
> 1. Metadata filtering for dept/access_level prevents cross-department data leakage
> 2. Parent-child indexing: small chunk for retrieval (256 tokens) → large chunk for generation (1024 tokens)
> 3. Hybrid search (BM25 + dense): recall improves 20-30% over pure dense search
>
> **Expected performance:** Retrieval < 200ms; E2E P95 < 3s (streaming); Faithfulness > 0.85

