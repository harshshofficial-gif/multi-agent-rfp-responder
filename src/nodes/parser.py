import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Import our schemas
from schemas import RFPRequirement, RFPState

load_dotenv()

# --- 1. Document Reader Helper ---

def read_docs(document_path: str) -> str:
    if document_path.endswith(".pdf"):
        # We can integrate pymupdf4llm here later
        import fitz  # or pymupdf4llm
        import pymupdf4llm
        return pymupdf4llm.to_markdown(document_path)
    elif document_path.endswith(".md") or document_path.endswith(".txt"):
        with open(document_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise ValueError("Unsupported file format. Please provide a PDF, Markdown, or text file.")

# --- 2. Structured Extraction Container ---

class ExtractedRequirements(BaseModel):
    """Container holding all parsed RFP requirements."""
    requirements: List[RFPRequirement] = Field(
        description="List of all extracted requirements, questions, and clauses."
    )

# --- 3. Prompt & Chain Setup ---

extraction_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert technical proposal auditor. "
        "Analyze the provided RFP document text and extract all actionable vendor obligations, "
        "technical questions, compliance standards, and mandatory clauses.\n\n"
        "Rules:\n"
        "1. Ignore company background, generic marketing narrative, and boilerplate introductions.\n"
        "2. For each requirement, assign an ID (e.g., REQ-001) if not explicitly present in the text.\n"
        "3. Set is_mandatory=True if language uses 'must', 'shall', 'required'. "
        "Set is_mandatory=False for 'prefer', 'should', 'optional'.\n"
        "4. Accurately categorize each item into TECHNICAL, SECURITY, COMPLIANCE, LEGAL, or PRICING."
    ),
    (
        "human",
        "Document Text:\n{document_text}\n"
    )
])

# Initialize LLM with structured output
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
structured_llm = llm.with_structured_output(ExtractedRequirements)
extraction_chain = extraction_prompt | structured_llm

# --- 4. The LangGraph Node Function ---

def parser_node(state: RFPState) -> RFPState:
    """Parser agent node that reads document text and populates requirements."""
    print("--- [Agent: Parser] Reading document and extracting requirements ---")
    
    # 1. Read document
    doc_text = read_docs(state.document_path)
    
    # 2. Extract structured requirements via LLM
    result: ExtractedRequirements = extraction_chain.invoke({"document_text": doc_text})
    
    # 3. Update the global graph state
    state.requirements = result.requirements
    state.current_stage = "retrieval"
    
    print(f"--- [Agent: Parser] Successfully extracted {len(state.requirements)} requirements ---")
    return state