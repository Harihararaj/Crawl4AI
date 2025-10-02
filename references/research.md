[Chunking](https://ai.gopubby.com/chunking-for-llms-windows-retrieval-and-cost-4e849378f834)
1. Use token aware chunking instead of character level.
2. Prefer using Recursive Text Splitters, which can preserve the sentences and paragraphs to some extend
3. Keep budgetting in mind when chunking
- Check what is the maximum context window that we set
- Count the tokens already used by Instructions, Guardrails etc
- Now calculate the remaining token available for context. Set the chunk size based on that also set the overlay to preserve natural flow.
- Based on the chunk size, decide how many chunks are going to be included in the context.
![ChunkingTypes](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*DK7ioZtQsUpArrZoXeDAzQ.png)

[RAG](https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4)
## Advanced Query Transformations:
### Multi Query (User Query Augumentation)  - RAG Fusion (Powerful)
- Single query can miss chunks because of synonyms miss match.
- Retreival can be made better by using LLM to augument questions, efficiently searching from various angles
- Fetch unique chunks for each of the question and re-rank them based on **Reciprocal Rank Fusion (RRF)**.
### Decomposition:
- User questions is decomposed into sub-questions that can be answered individually in multiple LLM pass and finally all the QA pair is sent for the final answer.
-  By breaking the question, we can generate more detailed answer than we did with normal RAG.
### Step Back Prompting:
- Sometimes user is so specific and our documents are more general, due to this our retrieval may be bad.
- Stepback prompting instructs the LLM to generate a more general question and perform retrieval from both original and formed general question. This provides more richer context for the LLM to generate the final answer.
- Teach this pattern to LLM by few shot prompting.
### HyDE (Hypothetical Decoment Embedding):
- First allow LLM to generate **Hypothetical** answer to the question. This answer may be factually wrong, but semantically rich.
- Embed the semantically rich answer to fetch the chunks and use this as a context to answer the question.
## Routing and Query Construction:
### Logical Routing:
- Querying all data source is inefficient, instead use LLM, give it the set of datasource and let it decide, which datasource to use (Use Pydantic to define the schema of various datasources).
### Semantic Routing:
- Sometimes we need to provide different prompts to LLM based on the question, like maths problems need more step-by-step procedure. So semantically find the similar prompt for the question using cosine similarity and use that prompt.
## Query Structuring:
- Not all the questions can be answered by just vector search, some times we need to filter based on the metadata. At that time use Pydantic to show the schema and description and allow the LLM to populate value for the filter, later structured query need to generated based on the values. This is an hybrid search where we need to perform vector search as well and filter based on the metadata.
## Advanced Indexing Strategy:
- Individual small chunks are good, but they lack the broader context needed for LLM. Broader chunks provide more context, but they perform poorly in the retrieval because their core idea gets diluted.
### Multi-representation Indexing:
- Instead of embedding the documents chunks, we create more smaller, more focused representation of each chunk (Summaries). Embed this summaries and perform vector similarity on this summaries. Use sepeate collections for the summaries and actual chunks, connect both by Id's. 
- After retrieving related summaries, retrieve the actual chunks itself and provide the chunks as a context. This makes the retrieval better.
## RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval):
- As the name implies, instead of one level of summaries. RAPTOR clusters the chunks, then sumaries the cluster, later this cluster summary is again clustered, and this process repeats till forming the root summary.
- WHen searching, you can search is various levels of this tree, allowing retrieval can be generic to specific. This is advanced technique.
![RAPTOR_Architecture](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*95v0K13O2rvsAYJ96ldhew.png)

## Token-Level Precision (ColBERT):
- Where we use ColBERT, that takes whole document, chunks and creates token level embeddings that is aware of whole document context.
- Laters query is embedded at token level and similarity is checked between token embeddings of chunks and query, and returns most similar chunks, this is more like a text similarity search.

## Advanced Retrieval & Generation:
### Dedicated Re-ranking
- Use CohereRerank model to rerank the retrieved chunks. This will return the score for the each chunk or document passed.

### Self-Correction using AI Agents (Corrective RAG and Self-RAG):
What if our RAG system could check its own work before giving an answer? That’s the idea behind self-correcting RAG architectures like CRAG (Corrective RAG) and Self-RAG.
![Architecture](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*LpQrsvNj09aJPMhhh4fc-A.png)

> [!IMPORTANT]
> Now Context windows for LLM have grown like 128k, 200k, even millions, Though passing the whole document is not feasible because relevant context may be diluted and lost in the big document, its hard for LLM to find that and answer the question. Long context are helpful when we really have more information to provide to LLM. So use the context window wise see if its actually needed.

## RAG Evaluation:
### Metrics:
- **Correctness** - Check whether our RAG pipeline correctly generates the expected answer (input: rag_output, expected_output)
- **Faithfulness** - metrics for whether output can be deduced from the context retrieved by RAG - This is the measure of relevance of the retrieved context (input: rag_output, expected_output, retrieved_context)

## Manual Evaluation:
In manual evaluation, LLM can be used as a judge to score between 0 to 1 for the correctness and faithfulness. This behaviour is acheived with properly prompting LLM to act as a judge, prompt should be different for correctness and the faithfulness.

Either evaluation pipeline can be created groundup, or use already existing evaluation tools like:
- **deepeval**
- **grouse**
- **RAGAS** (Specifically for RAG - Preferred)

