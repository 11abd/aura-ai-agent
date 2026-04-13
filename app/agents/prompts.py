from langchain_core.prompts import PromptTemplate


def get_planner_prompt():
    """
    Prompt for planning steps based on user goal
    """

    template = """
You are an AI planning agent.

Break the user's goal into clear, step-by-step actions.

Rules:
- Be logical and structured
- Keep steps concise
- Maximum 5 steps
- Each step should be actionable

User Goal:
{goal}

Output format:
1. Step one
2. Step two
3. Step three
"""

    return PromptTemplate(
        input_variables=["goal"],
        template=template
    )

def get_generator_prompt():
    """
    Prompt for resume tailoring
    """

    template = """
You are an expert resume optimizer.

Given:
1. Candidate Resume
2. Job Descriptions

Your task:
- Tailor the resume to match the job requirements
- Highlight relevant skills
- Improve keywords for ATS systems
- Keep it professional and concise

Candidate Resume:
{resume}

Job Context:
{context}

Output:
- Updated resume content
"""

    return PromptTemplate(
        input_variables=["resume", "context"],
        template=template
    )

def get_critic_prompt():
    """
    Prompt for evaluating generated resume
    """

    template = """
You are an expert resume reviewer.

Evaluate the resume based on:
- Relevance to job description
- Keyword optimization
- Clarity and structure
- Technical alignment

Job Context:
{context}

Generated Resume:
{resume}

Return:
- Score (0 to 10)
- Feedback with improvements
"""

    return PromptTemplate(
        input_variables=["context", "resume"],
        template=template
    )


def get_tool_selection_prompt():
    """
    Prompt to decide which tool to use
    """

    template = """
You are an intelligent agent.

Available tools:
1. rag → for internal knowledge (resume + stored jobs)
2. web_search → for real-time or missing information

Decide which tool is best for the query.

Rules:
- Use rag if query matches stored job data
- Use web_search if query needs fresh or unknown info

Query:
{query}
"""

    return PromptTemplate(
        input_variables=["query"],
        template=template
    )