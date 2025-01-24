from typing import Annotated, Callable, Literal

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command

from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

from prompts import *
from constants import DOCUMENT_TYPES
from functools import partial


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    doc: str
    document_type: str

graph_builder = StateGraph(State)

model_name = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)

def complaint_extractor_agent(state: State):
    print("complaint_e")
    return {"messages": [llm.invoke(complaint_extraction_prompt(state["messages"]))]}

def complaint_summarizer_agent(state: State):
    print("complaint_s")
    doc = state["messages"][0].content
    return {"messages": [llm.invoke(complaint_combined_prompt(state["messages"], doc))]}

def settlement_extractor_agent(state: State):
    print("settlement_e")
    return {"messages": [llm.invoke(settlement_extraction_prompt(state["messages"]))]}

def settlement_summarizer_agent(state: State):
    print("settlement_s")
    doc = state["messages"][0].content
    return {"messages": [llm.invoke(settlement_combined_prompt(state["messages"], doc))]}

def router_agent(state: State) -> Literal["complaint_extractor", "settlement_extractor"]:
    return f"{state['document_type']}_extractor"


def build_langgraph_flow():
    graph_builder.add_node("complaint_extractor", complaint_extractor_agent)
    graph_builder.add_node("complaint_summarizer", complaint_summarizer_agent)
    graph_builder.add_node("settlement_extractor", settlement_extractor_agent)
    graph_builder.add_node("settlement_summarizer", settlement_summarizer_agent)


    graph_builder.add_conditional_edges(START, router_agent, {
        "complaint_extractor": "complaint_extractor",
        "settlement_extractor": "settlement_extractor"
    })
    graph_builder.add_edge("complaint_extractor", "complaint_summarizer")
    graph_builder.add_edge("settlement_extractor", "settlement_summarizer")
    graph_builder.add_edge("settlement_summarizer", END)
    graph_builder.add_edge("complaint_summarizer", END)


    graph = graph_builder.compile()
    with open("example_graph.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
    return graph

def stream_graph_updates(graph, doc: str, doc_type: str):
    for event, metadata in graph.stream({"messages": [{"role": "user", "content": doc}], "document_type": doc_type}, stream_mode="messages"):
        if "summarizer" in metadata["langgraph_node"]:
            yield event.content
