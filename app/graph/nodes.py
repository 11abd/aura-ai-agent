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
            "reason": result.get("reason"),
            "context_preview": result["context"][:300],
            "context": result["context"]
        })
        logger.save_artifact("research_context", result["context"], "md")

    return {"context": result["context"]}


def generator_node(state):
    attempt = state.get("retries", 0) + 1
    resume = generator.generate_resume(
        state["context"],
        critic_feedback=state.get("feedback") or "",
        retry_count=state.get("retries", 0)
    )

    logger = state.get("logger")
    if logger:
        logger.log("generator", {
            "attempt": attempt,
            "used_feedback": bool(state.get("feedback")),
            "resume_preview": resume[:300],
            "resume_markdown": resume
        })
        logger.save_artifact(f"generated_resume_attempt_{attempt}", resume, "md")

    return {"generated_resume": resume}


def critic_node(state):
    attempt = state["retries"] + 1
    evaluation = critic.evaluate(state["context"], state["generated_resume"])

    result = {
        "score": evaluation.score,
        "feedback": evaluation.feedback,
        "retries": attempt
    }

    logger = state.get("logger")
    if logger:
        logger.log("critic", {
            "attempt": attempt,
            "score": evaluation.score,
            "verdict": evaluation.verdict,
            "role_fit": evaluation.role_fit,
            "truthfulness": evaluation.truthfulness,
            "keyword_alignment": evaluation.keyword_alignment,
            "clarity": evaluation.clarity,
            "strategic_emphasis": evaluation.strategic_emphasis,
            "strengths": evaluation.strengths,
            "risks": evaluation.risks,
            "improvements": evaluation.improvements,
            "feedback": evaluation.feedback
        })
        logger.save_artifact(
            f"critic_evaluation_attempt_{attempt}",
            "\n".join([
                f"# Critic Evaluation Attempt {attempt}",
                f"- Overall score: {evaluation.score}/10",
                f"- Verdict: {evaluation.verdict}",
                f"- Role fit: {evaluation.role_fit}/10",
                f"- Truthfulness: {evaluation.truthfulness}/10",
                f"- Keyword alignment: {evaluation.keyword_alignment}/10",
                f"- Clarity: {evaluation.clarity}/10",
                f"- Strategic emphasis: {evaluation.strategic_emphasis}/10",
                "",
                "## Strengths",
                evaluation.strengths,
                "",
                "## Risks",
                evaluation.risks,
                "",
                "## Improvements",
                evaluation.improvements,
                "",
                "## Summary",
                evaluation.feedback,
            ]),
            "md"
        )

    memory.save({
        "query": state["query"],
        "score": evaluation.score,
        "verdict": evaluation.verdict,
        "feedback": evaluation.feedback
    })
    return result
