from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes import (
    planner_node,
    research_node,
    generator_node,
    critic_node
)
from app.graph.edges import should_retry


def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("research", research_node)
    graph.add_node("generator", generator_node)
    graph.add_node("critic", critic_node)

    # Flow
    graph.set_entry_point("planner")

    graph.add_edge("planner", "research")
    graph.add_edge("research", "generator")
    graph.add_edge("generator", "critic")

    # Conditional edge 🔥
    graph.add_conditional_edges(
        "critic",
        should_retry,
        {
            "retry": "generator",
            "end": END
        }
    )

    return graph.compile()