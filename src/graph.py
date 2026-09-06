from schemas import RFPState 
from langgraph.graph import StateGraph, START, END

def parser_node(state: RFPState) -> RFPState:
    # Define the parser node
    print("---RUNNING PARSER NODE---")
    return state

def retriever_node(state: RFPState) -> RFPState:
    # Define the retriever node
    print("---RUNNING RETRIEVER NODE---")
    return state

def drafter_node(state: RFPState) -> RFPState:
    # Define the drafter node
    print("---RUNNING DRAFTER NODE---")
    return state

def compliance_node(state: RFPState) -> RFPState:
    # Define the compliance node
    print("---RUNNING COMPLIANCE NODE---")
    return state

builder = StateGraph(RFPState)

builder.add_node("parser", parser_node)
builder.add_node("retriever", retriever_node)
builder.add_node("compliance", compliance_node)
builder.add_node("drafter", drafter_node)

builder.add_edge(START, "parser")
builder.add_edge("parser", "retriever")
builder.add_edge("retriever", "drafter")
builder.add_edge("drafter", "compliance")
builder.add_edge("compliance", END)

app = builder.compile()

if __name__ == "__main__":
    initial_state = RFPState(document_path="sample_rfps/sample.pdf")
    final_output = app.invoke(initial_state)
    print("\nGraph execution completed.")
    print(f"Final State Stage: {final_output['current_stage']}")