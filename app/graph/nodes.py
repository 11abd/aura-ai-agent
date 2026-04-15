from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.generator_agent import GeneratorAgent
from app.agents.critic_agent import CriticAgent
from app.memory.memory_service import MemoryService

planner = PlannerAgent()
researcher = ResearchAgent()
generator = GeneratorAgent()
critic = CriticAgent()
memory = MemoryService()


def planner_node(state):
    plan = planner.create_plan(state["query"])

    logger = state.get("logger")
    if logger:
        logger.log("planner", {
            "query": state["query"],
            "plan": plan
        })

    return {"plan": plan}


def research_node(state):
    result = researcher.research(state["query"])
    
    logger = state.get("logger")
    if logger:
        logger.log("research", {
            "tool_used": result.get("tool_used"),
            "context_preview": result["context"][:300]
        })

    return {"context": result["context"]}


def generator_node(state):
    resume = generator.generate_resume(state["context"])

    logger = state.get("logger")
    if logger:
        logger.log("generator", {
            "resume_preview": resume[:300]
        })


    return {"generated_resume": resume}
   


def critic_node(state):
    evaluation = critic.evaluate(state["context"], state["generated_resume"])

    result = {
        "score": evaluation.score,
        "feedback": evaluation.feedback,
        "retries": state["retries"] + 1
    }

    logger = state.get("logger")
    if logger:
        logger.log("critic", {
            "score": evaluation.score,
            "feedback": evaluation.feedback
        })

    memory.save({
        "query": state["query"],
        "score": evaluation.score,
        "feedback": evaluation.feedback
    })
    return result