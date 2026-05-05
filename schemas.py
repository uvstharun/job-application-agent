from pydantic import BaseModel, Field
from typing import TypedDict, Optional


class JobRequirements(BaseModel):
    required_skills: list[str] = Field(
        description="Skills explicitly required in the job description"
    )
    nice_to_have_skills: list[str] = Field(
        description="Skills mentioned as preferred but not required"
    )
    years_experience: str = Field(
        description="Years of experience required e.g. 3-5 years"
    )
    key_responsibilities: list[str] = Field(
        description="Main responsibilities of the role"
    )
    keywords: list[str] = Field(
        description="Important keywords and phrases from the job description"
    )
    seniority_level: str = Field(
        description="Junior, Mid, Senior, Staff, Principal etc"
    )



class ResumeProfile(BaseModel):
    current_skills: list[str] = Field(
        description="All technical and soft skills present in the resume"
    )
    years_experience: str = Field(
        description="Total years of relevant experience"
    )
    key_achievements: list[str] = Field(
        description="Notable achievements and impact statements"
    )
    keywords_present: list[str] = Field(
        description="Keywords from the resume that match industry terminology"
    )
    current_role: str = Field(
        description="Current or most recent job title"
    )

class FitAnalysis(BaseModel):
    fit_score: int = Field(
        description="Overall fit score from 0 to 100"
    )
    strengths: list[str] = Field(
        description="Areas where the candidate strongly matches the job"
    )
    skill_gaps: list[str] = Field(
        description="Required skills missing from the resume"
    )
    reasoning: str = Field(
        description="2-3 sentences explaining the fit score"
    )

class TailoringAdvice(BaseModel):
    resume_edits: list[str] = Field(
        description="Specific bullet point suggestions to add or rewrite"
    )
    keywords_to_add: list[str] = Field(
        description="Keywords from the JD missing from the resume"
    )
    cover_letter_opening: str = Field(
        description="A strong opening paragraph for the cover letter"
    )
    interview_prep: list[str] = Field(
        description="Likely interview questions based on the job description"
    )

class UpskillingPlan(BaseModel):
    critical_gaps: list[str] = Field(
        description="The most important missing skills to address first"
    )
    learning_resources: list[str] = Field(
        description="Specific courses or resources for each critical gap"
    )
    realistic_timeline: str = Field(
        description="Honest estimate of time needed to become competitive"
    )
    apply_now_anyway: bool = Field(
        description="Whether to apply despite gaps — sometimes worth it"
    )
    apply_reasoning: str = Field(
        description="Reasoning for whether to apply now or wait"
    )


# -------------------------------------------------------
# LANGGRAPH STATE
# This is the shared whiteboard every node reads and writes.
# Every field starts empty except job_description and resume.
# -------------------------------------------------------

class AgentState(TypedDict):
    job_description: str
    resume: str
    job_requirements: Optional[dict]
    resume_profile: Optional[dict]
    fit_score: Optional[int]
    skill_gaps: Optional[list]
    strengths: Optional[list]
    tailoring_advice: Optional[dict]
    upskilling_plan: Optional[dict]
    final_report: Optional[str]