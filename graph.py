from langgraph.graph import StateGraph, END
from schemas import AgentState
from node import (
    extract_job_requirements,
    extract_resume_profile,
    analyze_fit,
    generate_tailoring,
    generate_upskilling,
    compile_report,
    route_by_fit_score
)

def build_graph():
    # Step 1 — Create the graph with our state type
    graph = StateGraph(AgentState)

    # Step 2 — Register all nodes
    graph.add_node("extract_job_requirements", extract_job_requirements)
    graph.add_node("extract_resume_profile", extract_resume_profile)
    graph.add_node("analyze_fit", analyze_fit)
    graph.add_node("generate_tailoring", generate_tailoring)
    graph.add_node("generate_upskilling", generate_upskilling)
    graph.add_node("compile_report", compile_report)

    # Step 3 — Set the entry point
    graph.set_entry_point("extract_job_requirements")

    # Step 4 — Regular edges — always flow this way
    graph.add_edge("extract_job_requirements", "extract_resume_profile")
    graph.add_edge("extract_resume_profile", "analyze_fit")

    # Step 5 — Conditional edge — routes based on fit_score
    graph.add_conditional_edges(
        "analyze_fit",
        route_by_fit_score,
        {
            "strong": "generate_tailoring",
            "weak": "generate_upskilling"
        }
    )

    # Step 6 — Both paths lead to compile_report
    graph.add_edge("generate_tailoring", "compile_report")
    graph.add_edge("generate_upskilling", "compile_report")

    # Step 7 — compile_report is the final node
    graph.add_edge("compile_report", END)

    # Step 8 — Compile and return
    return graph.compile()


# Create the app — ready to invoke
app = build_graph()