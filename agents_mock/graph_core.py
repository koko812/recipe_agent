# graph_core.py
from typing import Dict, Any, List
from schemas import RecipeQuery, Plan, RecipeCandidate, AgentReply
from tools.recipe_search import find_recipes_mock

def planner(state: Dict[str, Any]) -> Dict[str, Any]:
    q: RecipeQuery = state["query"]
    plan_steps = ["材料の正規化", "候補レシピの収集", "制約でリランキング", "要約生成"]
    state["plan"] = Plan(steps=plan_steps)
    return state

def router(state: Dict[str, Any]) -> Dict[str, Any]:
    state["selected_tool"] = "recipe_search"
    return state

def tool_exec(state: Dict[str, Any]) -> Dict[str, Any]:
    q: RecipeQuery = state["query"]
    if state.get("selected_tool") == "recipe_search":
        state["candidates"] = find_recipes_mock(q)
    return state

def respond(state: Dict[str, Any]) -> Dict[str, Any]:
    cands: List[RecipeCandidate] = state.get("candidates", [])
    best = max(cands, key=lambda x: x.score) if cands else None
    explanation = f"主材料: {', '.join(state['query'].ingredients)}。制約: {', '.join(state['query'].constraints)}。"
    answer = f"おすすめは「{best.title}」。ポイント: {best.summary}\nURL: {best.url}" if best else "該当なしでした"
    state["reply"] = AgentReply(plan=state["plan"], choices=cands, final_answer=explanation + "\n" + answer)
    return state

NODES = [planner, router, tool_exec, respond]

def run_graph(query: RecipeQuery) -> AgentReply:
    state: Dict[str, Any] = {"query": query}
    for node in NODES:
        state = node(state)
    return state["reply"]

