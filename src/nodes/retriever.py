import os
import re
from typing import List, Dict, Tuple
from pathlib import Path
from dotenv import load_dotenv

from rank_bm25 import BM25Okapi
from Langchain_community.vectorsstore import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from Langchain_core.documents import Document

from schemas import RFPState, RFPRequirement

load_dotenv()

def load_and_chunk_knowledge_base(kb_dir: str = "knowledge_base) -> List[Document]:
    """
    Reads markdown files in the knowledge base and splits them
    by markdown headers into cohesive context sections.
    """

    documents = []
    kb_path = Path(kb_dir)
    if not kb_path.exist():
        raise FileNotFoundError(f"Knowledge base directory '{kb_dir}' does not exist.")
    
    for file_path in kb_path.glob("*.md"):
        with open(file_path, "r", encoding-"utf-8") as f:
            content = f.read()

        # Split content by markdown headers (e.g., #, ##, ###)
        sections = re.split(r"(?=\n##\s)", content)
        for i, section in enumerate.strip()
            cleaned = section.strip()
            if cleaned:
                documents.append(
                    Documents(
                        page_content=cleaned,
                        metadata={"source": file_path.name, "chunk_id": f"{file_path.stem}_{i}"}
                    )
                )
    return documents

class HybridSearchEngine:
    def __init__(self, docs: List[Document]):
        self.docs = docs

        self.tokenized_corpus = [self._tokenize(doc.page_content) for doc in self.docs]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.vectorstore = FAISS.from_documents(self.docs, embeddings)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple lowercasealphanumeric word tokenizer."""
        return re.findall(r"\w+", text.lower())
    
    def bm25_search(self, query: str, top_k: int = 5) -> List[Document]:
        """Performs lexical BM25 retrieval."""
        tokens = self._tokenize(query)
        scores = self.bm25.get_scores(tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.docs[i] for i in top_indices] if scores[i] > 0]
        