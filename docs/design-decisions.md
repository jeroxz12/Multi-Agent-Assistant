# Design decisions

These are the choices that define v0.1.0. The defaults live in code, mostly in `src/config.py`. Changing a default does not require a new architecture. Limitations are part of the choice, not a backlog in disguise.

## LCEL and RunnableBranch

The router is a LangChain pipeline. `|` passes the output of one step into the next. `RunnablePassthrough.assign` adds the classifier result without dropping the question. `RunnableBranch` runs the first condition that matches.

The classifier uses `with_structured_output(RouteDecision)`, so the model must return `department`, `confidence`, and `reason`. The evaluator uses the same pattern for `QualityScores`. A validator divides a confidence such as `90` by 100 and clamps the result to 0–1.

This keeps one question on one branch, and it gives Langfuse a stable name for each step: `orchestrator`, `router`, `rag_hr`, `rag_tech`, `rag_finance`, `retriever`, `generation`, and `evaluator`.

The router is not a tool-calling loop, and it does not use LangGraph. It cannot decide mid-retrieval to switch departments. A question that truly needs two departments gets one of them, using the access-over-policy rule in the classifier prompt.

`build_router()` constructs all three RAG chains before the branch runs. Construction opens store clients. Only the selected branch retrieves and generates.

## One Pinecone index and three namespaces

`hr`, `tech`, and `finance` are namespaces of a single index, `multi-agent-assistant`. A search in `hr` does not see `finance` vectors. The metric is cosine, and each vector has 1536 dimensions, matching `text-embedding-3-small`.

One index is enough for three small collections and keeps a single host and key. The cost is that a new embedding dimension cannot be mixed into the existing index. `ensure_index` returns immediately when the index name already exists, so a dimension change means creating a new index and ingesting again.

Ingest deletes the whole namespace and upserts it from Markdown. That makes `data/` the source of truth and avoids stale chunks after an edit. It also means a partial update is not supported: one changed file rewrites every vector in that namespace.

## Grounded answers and a fixed top k

Each agent receives the top `retriever_k` chunks, currently 4. Retrieval always returns that many chunks. The prompt, not a score cutoff, tells the model to say when the documents do not cover the question.

Chunks are 800 characters with 120 characters of overlap (`RecursiveCharacterTextSplitter`). The overlap keeps a sentence that crosses a cut available in both chunks. Policies were added as Markdown files when a domain needed more source text. The splitter settings were not reduced to manufacture more chunks.

`gpt-4o-mini` is called with temperature 0 in the classifier, the RAG chain, and the evaluator. The temperature is set on each `ChatOpenAI` instance. It is not a field on `Settings`.

A fixed k can pull a weak fourth chunk into the prompt. Temperature 0 makes repeated manual checks easier to compare, and it does not make the answer factually certain.

## Confidence threshold of 0.6

`route_confidence_threshold` is `0.6`. Below that value, no RAG branch runs and the user is asked to say whether the topic is people, system access, or payments.

The threshold is a product rule, not a calibrated probability. The classifier can be confidently wrong and still pass. Low-confidence questions share the public department `out_of_scope` with truly out-of-scope questions. The refusal text is what distinguishes them.

## FastAPI and a static page

`src/api.py` is a thin translation of HTTP into `answer()`. The page is HTML, CSS, and JavaScript served by the same process. There is no second client stack.

That is enough for a local demo. The API has no authentication, no rate limit, and no conversation id. Anyone who can reach the port can spend OpenAI and Pinecone quota.

## Evaluator after the answer

For `hr`, `tech`, and `finance`, a second model call grades the question, the answer, and the retrieved excerpts. It does not replace the answer. Scores are written with the Langfuse score API on the trace that just finished.

Out-of-scope refusals are not graded. There was no retrieved context to judge, and a refusal is not a failed RAG answer.

The grades are model judgments. They are not a human gold set, and a high score does not prove the policy text is legally correct. If the documents are silent and the answer says so, the evaluator prompt allows accuracy to stay high.

Direct department commands skip this step. Only `answer()` scores.

## Single turn

`answer()` does not read or write conversation history. Each question is classified on its own. Follow-ups such as "and in Chile?" have no previous department to reuse.

That keeps the trace and the API contract small. It also makes a multi-step HR conversation start over on every message.
