import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import RFPState 
from langgraph.graph import StateGraph, START, END
from nodes.parser import parser_node

def retriever_node(state: RFPState) -> RFPState:
    print("---RUNNING RETRIEVER NODE---")
    state.current_stage = "drafting"
    return state

def drafter_node(state: RFPState) -> RFPState:
    print("---RUNNING DRAFTER NODE---")
    state.current_stage = "compliance"
    return state

def compliance_node(state: RFPState) -> RFPState:
    print("---RUNNING COMPLIANCE NODE---")
    state.current_stage = "completed"
    return state

builder = StateGraph(RFPState)

builder.add_node("parser", parser_node)
builder.add_node("retriever", retriever_node)
builder.add_node("drafter", drafter_node)
builder.add_node("compliance", compliance_node)

builder.add_edge(START, "parser")
builder.add_edge("parser", "retriever")
builder.add_edge("retriever", "drafter")
builder.add_edge("drafter", "compliance")
builder.add_edge("compliance", END)

app = builder.compile()

if __name__ == "__main__":
    initial_state = RFPState(document_path="sample_rfps/test_rfp.md")
    final_output = app.invoke(initial_state)
    requirements = final_output.get("requirements", [])
    
    print("\n=========================================")
    print("--- Pipeline Completed Successfully! ---")
    print(f"Total Requirements Extracted: {len(requirements)}")
    print("==========================================\n")
    
    for req in requirements:
        print(f"[{req.id}] ({req.category}) Mandatory: {req.is_mandatory}")
        print(f"Clause: {req.raw_text}")
        print("-" * 50)