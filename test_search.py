# import re

# from pydantic import FilePath
# from rank_bm25 import BM25Okapi

# documents = [
#     "All data at rest is secured via AES-256 encryption.",
#     "We utilize industry-standard cryptographic algorithms to protect stored client information.",
#     "Our disaster recovery policy guarantees an RTO under 1 hour."
# ]

# tokenized_docs = []
# for doc in documents:
#     words = doc.lower().replace(".", "").split()
#     tokenized_docs.append(words)

# print("First document as words:", tokenized_docs[0])

# bm25_index = BM25Okapi(tokenized_docs)
# query = "AES-256 encryption"
# tokenized_query = query.lower().split(" ")
# scores = bm25_index.get_scores(tokenized_query)

# print("\n--- BM25 Scores ---")
# for i in range(len(documents)):
#     print(f"Score: {scores[i]:.4f} --> {documents[i]}")

# import os
# from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS



# print("\n --- Testing Dense Vector Search ---")

# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# vector_db = FAISS.from_texts(documents, embeddings)
# concept_query = "How do you protect stored client information?"
# results = vector_db.similarity_search_with_score(concept_query, k=3)
# for doc, score in results:
#     print(f"Distance Score: {score:.4f} --> {doc.page_content}")

# print("\n --- Combining with Reciprocal Rank Fusion (RRF) ---")

# bm25_ranked = [
#     "All data at rest is secured via AES-256 encryption."
# ]

# vector_ranked = [
#     "We utilize industry-standard cryptographic algorithms to protect stored client information.",
#     "All data at rest is secured via AES-256 encryption.",
#     "Our disaster recovery policy guarantees an RTO under 1 hour."
# ]

# k = 60
# rrf_scores = {}
# for rank, text in enumerate(bm25_ranked, start=1):
#     rrf_scores[text] = rrf_scores.get(text, 0.0) + (1.0 / (k + rank))

# for rank, text in enumerate(vector_ranked, start=1):
#     rrf_scores[text] = rrf_scores.get(text, 0.0) + (1.0 / (k + rank))

# sorted_by_rrf = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
# for text, score in sorted_by_rrf:
#     print(f"RRF Score: {score:.5f} --> {text}")


# def fuse_ranks(list_1, list_2, k=60):
#     scores = {}
#     for rank, doc in enumerate(list_1, start=1):
#         score_to_add = 1.0 / (k + rank)
        
#         scores[doc] = scores.get(doc, 0.0) + score_to_add


#     for rank, doc in enumerate(list_2, start=1):
#         score_to_add = 1.0 / (k+rank)
#         scores[doc] = scores.get(doc, 0.0) + score_to_add

#     sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse = True)
#     return sorted_docs

# with open(FilePath, mode="r", encoding="utf-8") as f:
#     full_text = f.read()
#     raw_sections = re.split(r"\n##", full_text)
#     cleaned = [section.strip() for section in raw_sections if section.strip()]

import re
from rank_bm25 import BM25Okapi
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Your File Reader & Chunker
def load_policy_chunks(file_path):
    with open(file_path, mode="r", encoding="utf-8") as f:
        full_text = f.read()
    raw_sections = re.split(r"\n##", full_text)
    return [section.strip() for section in raw_sections if section.strip()]

# 2. Your RRF Function
def fuse_ranks(list_1, list_2, k=60):
    scores = {}
    for rank, doc in enumerate(list_1, start=1):
        scores[doc] = scores.get(doc, 0.0) + (1.0 / (k + rank))
    for rank, doc in enumerate(list_2, start=1):
        scores[doc] = scores.get(doc, 0.0) + (1.0 / (k + rank))
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)

# --- EXECUTION ---
# Load real chunks from our knowledge base
chunks = load_policy_chunks("knowledge_base/company_policies.md")
print(f"Loaded {len(chunks)} sections from knowledge base.")

# Build BM25
tokenized_corpus = [chunk.lower().split() for chunk in chunks]
bm25 = BM25Okapi(tokenized_corpus)

# Build FAISS Vector Store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.from_texts(chunks, embeddings)

# Test Query: One of our actual RFP requirements!
query = "All customer data at rest must be encrypted using AES-256 keys managed via a dedicated HSM or cloud KMS."

# 1. BM25 Search
bm25_scores = bm25.get_scores(query.lower().split())
# Get top 3 chunks sorted by BM25 score
bm25_top_indices = sorted(range(len(chunks)), key=lambda i: bm25_scores[i], reverse=True)[:3]
bm25_results = [chunks[i] for i in bm25_top_indices]

# 2. Vector Search (Top 3)
vector_results = [doc.page_content for doc in vector_db.similarity_search(query, k=3)]

# 3. Fuse with your RRF function!
fused = fuse_ranks(bm25_results, vector_results)

print("\n--- Top Retrieved Chunk via RRF ---")
top_chunk, top_score = fused[0]
print(f"RRF Score: {top_score:.5f}")
print(top_chunk)