import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas import (
    AgentState, JobRequirements, ResumeProfile,
    FitAnalysis, TailoringAdvice, UpskillingPlan
)
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------
# LLM SETUP
# One shared LLM instance used by all nodes.
# -------------------------------------------------------

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    max_tokens=2048
)

# -------------------------------------------------------
# HELPER FUNCTION
# Builds a LangChain chain for structured extraction.
# Same pattern you used in the clinical note summarizer.
# -------------------------------------------------------

def build_chain(pydantic_model, system_prompt: str, human_prompt: str):
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt + "\n\n{format_instructions}"),
        ("human", human_prompt)
    ])
    return prompt | llm | parser, parser


# -------------------------------------------------------
# NODE 1 — EXTRACT JOB REQUIREMENTS
# Reads: job_description
# Writes: job_requirements
# -------------------------------------------------------

def extract_job_requirements(state: AgentState) -> dict:
    print("Node 1: Extracting job requirements...")

    chain, parser = build_chain(
        JobRequirements,
        """You are an expert job description analyzer.
        Extract structured requirements from the job description.
        Be precise and complete. Include all mentioned skills.""",
        "Analyze this job description:\n\n{job_description}"
    )

    result = chain.invoke({
        "job_description": state["job_description"],
        "format_instructions": parser.get_format_instructions()
    })

    return {"job_requirements": result.model_dump()}


# -------------------------------------------------------
# NODE 2 — EXTRACT RESUME PROFILE
# Reads: resume
# Writes: resume_profile
# -------------------------------------------------------

def extract_resume_profile(state: AgentState) -> dict:
    print("Node 2: Extracting resume profile...")

    chain, parser = build_chain(
        ResumeProfile,
        """You are an expert resume analyzer.
        Extract structured information from the resume.
        Be objective and precise about skills and experience.""",
        "Analyze this resume:\n\n{resume}"
    )

    result = chain.invoke({
        "resume": state["resume"],
        "format_instructions": parser.get_format_instructions()
    })

    return {"resume_profile": result.model_dump()}


# -------------------------------------------------------
# NODE 3 — ANALYZE FIT
# Reads: job_requirements, resume_profile
# Writes: fit_score, skill_gaps, strengths
# -------------------------------------------------------

def analyze_fit(state: AgentState) -> dict:
    print("Node 3: Analyzing fit...")

    chain, parser = build_chain(
        FitAnalysis,
        """You are an expert career coach and recruiter.
        Compare the job requirements against the candidate's profile.
        Give an honest fit score from 0 to 100.
        A score of 60 or above means the candidate should apply.
        Be specific about gaps and strengths.""",
        """Job Requirements:
{job_requirements}

Candidate Profile:
{resume_profile}

Analyze the fit between this candidate and this role."""
    )

    result = chain.invoke({
        "job_requirements": json.dumps(state["job_requirements"], indent=2),
        "resume_profile": json.dumps(state["resume_profile"], indent=2),
        "format_instructions": parser.get_format_instructions()
    })

    return {
        "fit_score": result.fit_score,
        "skill_gaps": result.skill_gaps,
        "strengths": result.strengths
    }


# -------------------------------------------------------
# NODE 4A — GENERATE TAILORING ADVICE
# Runs when fit_score >= 60
# Reads: job_requirements, resume_profile, skill_gaps, strengths
# Writes: tailoring_advice
# -------------------------------------------------------

def generate_tailoring(state: AgentState) -> dict:
    print("Node 4a: Generating tailoring advice (strong fit path)...")

    chain, parser = build_chain(
        TailoringAdvice,
        """You are an expert resume writer and career coach.
        The candidate has a strong fit for this role.
        Give specific, actionable advice to maximize their chances.
        Resume edits should be concrete bullet points they can copy.
        The cover letter opening should be compelling and specific.""",
        """Job Requirements:
{job_requirements}

Candidate Profile:
{resume_profile}

Skill Gaps to Address:
{skill_gaps}

Key Strengths:
{strengths}

Provide specific tailoring advice to strengthen this application."""
    )

    result = chain.invoke({
        "job_requirements": json.dumps(state["job_requirements"], indent=2),
        "resume_profile": json.dumps(state["resume_profile"], indent=2),
        "skill_gaps": json.dumps(state["skill_gaps"], indent=2),
        "strengths": json.dumps(state["strengths"], indent=2),
        "format_instructions": parser.get_format_instructions()
    })

    return {"tailoring_advice": result.model_dump()}


# -------------------------------------------------------
# NODE 4B — GENERATE UPSKILLING PLAN
# Runs when fit_score < 60
# Reads: job_requirements, skill_gaps
# Writes: upskilling_plan
# -------------------------------------------------------

def generate_upskilling(state: AgentState) -> dict:
    print("Node 4b: Generating upskilling plan (weak fit path)...")

    chain, parser = build_chain(
        UpskillingPlan,
        """You are an honest career coach.
        The candidate has significant gaps for this role.
        Give them a realistic plan to become competitive.
        Be honest about timeline — don't sugarcoat it.
        Sometimes it is still worth applying even with gaps — say so if true.""",
        """Job Requirements:
{job_requirements}

Skill Gaps Identified:
{skill_gaps}

Create an honest upskilling plan for this candidate."""
    )

    result = chain.invoke({
        "job_requirements": json.dumps(state["job_requirements"], indent=2),
        "skill_gaps": json.dumps(state["skill_gaps"], indent=2),
        "format_instructions": parser.get_format_instructions()
    })

    return {"upskilling_plan": result.model_dump()}


# -------------------------------------------------------
# NODE 5 — COMPILE FINAL REPORT
# Reads: everything
# Writes: final_report
# -------------------------------------------------------

def compile_report(state: AgentState) -> dict:
    print("Node 5: Compiling final report...")

    fit_score = state["fit_score"]
    path = "STRONG FIT" if fit_score >= 60 else "NEEDS DEVELOPMENT"

    report = f"""
JOB APPLICATION ANALYSIS REPORT
{'='*50}

FIT SCORE: {fit_score}/100 — {path}

STRENGTHS:
{chr(10).join(f'  - {s}' for s in state['strengths'])}

SKILL GAPS:
{chr(10).join(f'  - {g}' for g in state['skill_gaps'])}
"""

    if fit_score >= 60:
        advice = state["tailoring_advice"]
        report += f"""
RESUME TAILORING SUGGESTIONS:
{chr(10).join(f'  - {e}' for e in advice['resume_edits'])}

KEYWORDS TO ADD:
{chr(10).join(f'  - {k}' for k in advice['keywords_to_add'])}

COVER LETTER OPENING:
  {advice['cover_letter_opening']}

LIKELY INTERVIEW QUESTIONS:
{chr(10).join(f'  - {q}' for q in advice['interview_prep'])}
"""
    else:
        plan = state["upskilling_plan"]
        report += f"""
CRITICAL SKILLS TO DEVELOP:
{chr(10).join(f'  - {g}' for g in plan['critical_gaps'])}

LEARNING RESOURCES:
{chr(10).join(f'  - {r}' for r in plan['learning_resources'])}

REALISTIC TIMELINE: {plan['realistic_timeline']}

SHOULD YOU APPLY NOW? {'Yes' if plan['apply_now_anyway'] else 'Not yet'}
REASONING: {plan['apply_reasoning']}
"""

    return {"final_report": report}


# -------------------------------------------------------
# ROUTING FUNCTION
# This is what the conditional edge calls.
# Reads fit_score from state and returns a string
# that maps to the next node.
# -------------------------------------------------------

def route_by_fit_score(state: AgentState) -> str:
    if state["fit_score"] >= 60:
        return "strong"
    return "weak"