from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.generator_agent import GeneratorAgent
from app.agents.critic_agent import CriticAgent

planner = PlannerAgent()
researcher = ResearchAgent()
generator = GeneratorAgent()
critic = CriticAgent()


def planner_node(state):
    plan = planner.create_plan(state["query"])
    return {"plan": plan}


def research_node(state):
    result = researcher.research(state["query"])
    return {"context": result["context"]}


def generator_node(state):
    resume = generator.generate_resume(state["context"])
    return {"generated_resume": resume}


def critic_node(state):
    evaluation = critic.evaluate(state["context"], state["generated_resume"])

    return {
        "score": evaluation.score,
        "feedback": evaluation.feedback,
        "retries": state["retries"] + 1
    }