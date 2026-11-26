from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.recruitment.resume_parser import parse_resume
from src.recruitment.evaluator import evaluate_candidate

class ScreeningState(TypedDict, total=False):
    resume_path: str
    job_description: str
    resume_text: str
    candidate_profile: dict
    evaluation: dict
    status: str

def parse_node(state: ScreeningState):
    parsed = parse_resume(state["resume_path"])
    return {"resume_text": parsed["resume_text"], "candidate_profile": parsed}

def evaluate_node(state: ScreeningState):
    return {"evaluation": evaluate_candidate(state["resume_text"], state["job_description"])}

def human_review_node(state: ScreeningState):
    return {"status": "review_required"}

def build_screening_graph():
    graph = StateGraph(ScreeningState)
    graph.add_node("resume_parser_agent", parse_node)
    graph.add_node("candidate_evaluation_agent", evaluate_node)
    graph.add_node("human_review_queue", human_review_node)
    graph.set_entry_point("resume_parser_agent")
    graph.add_edge("resume_parser_agent", "candidate_evaluation_agent")
    graph.add_edge("candidate_evaluation_agent", "human_review_queue")
    graph.add_edge("human_review_queue", END)
    return graph.compile()
