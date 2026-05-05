from graph import app

# -------------------------------------------------------
# SAMPLE JOB DESCRIPTION
# Using a Healthcare AI role — relevant to your goals
# -------------------------------------------------------

JOB_DESCRIPTION = """
Senior Healthcare AI Engineer
Company: HealthTech Solutions
Location: Los Angeles, CA (Hybrid)

About the Role:
We are looking for a Senior Healthcare AI Engineer to join our growing 
team building AI-powered clinical decision support tools for health systems 
across the US.

Required Skills:
- 4+ years of experience in data science or machine learning
- Strong Python programming skills
- Experience with LLMs and prompt engineering
- Experience building RAG pipelines
- Knowledge of healthcare data standards (HL7, FHIR, ICD-10)
- Experience with vector databases (Pinecone, ChromaDB, or similar)
- FastAPI or similar framework for building APIs
- SQL proficiency
- Experience with cloud platforms (AWS, Azure, or GCP)

Nice to Have:
- LangChain or LangGraph experience
- Experience with clinical NLP (spaCy, scispaCy)
- Knowledge of HIPAA compliance requirements
- Experience with EHR systems
- MLOps experience (MLflow, model monitoring)

Responsibilities:
- Build and maintain AI pipelines for clinical data processing
- Design and implement RAG systems over clinical documents
- Collaborate with clinical informaticists and physicians
- Deploy and monitor ML models in production
- Write technical documentation

Compensation: 150,000 to 180,000 USD annually
"""

# -------------------------------------------------------
# SAMPLE RESUME
# Based on your actual background
# -------------------------------------------------------

RESUME = """
VISHNU SAI
Data Scientist | Healthcare AI
LinkedIn: linkedin.com/in/vishnusai29
GitHub: github.com/uvstharun

EXPERIENCE

Data Scientist — LA County Department of Health Services (via Heluna Health)
2022 - Present
- Built SARIMAX bed utilization forecasting models across 4 hospitals
  with MAPE of 6.49% deployed to Azure Synapse Analytics
- Developed radiology KPI dashboards using Vertica SQL and Tableau
- Built outpatient specialty care provider roster using complex CTEs
  over 26.7 million Medicare prescribing records
- Created NL-to-SQL agent using Anthropic Claude API and SQLite
- Built ICD-10 code explainer with Pydantic structured outputs
- Built clinical note summarizer using LangChain and FastAPI

Data Scientist — Inova Health System
2020 - 2022
- Built fraud detection models using Isolation Forest and One-Class SVM
- Developed NLP pipelines using spaCy and NLTK on clinical text
- Created Tableau dashboards for hospital operations teams

SKILLS
Technical: Python, SQL (Vertica, SQLite), R, Tableau, Tableau Prep
AI/ML: LangChain, Anthropic Claude API, RAG pipelines, ChromaDB,
       Pydantic, FastAPI, SARIMAX, LSTM, Isolation Forest
Healthcare: ICD-10, CCSR, HL7 basics, EHR data, CMS Medicare data
Cloud: Azure Synapse Analytics, ADLS Gen2, Azure Databricks

PROJECTS
- Healthcare NL-to-SQL Agent: Multi-tool agent over 26.7M Medicare records
- ICD Code Explainer: Clinical coding AI with Pydantic structured outputs
- Clinical Note Summarizer: LangChain + Claude discharge summary extraction
"""

# -------------------------------------------------------
# RUN THE AGENT
# -------------------------------------------------------

if __name__ == "__main__":
    print("Starting Job Application Agent...")
    print("="*60)

    initial_state = {
        "job_description": JOB_DESCRIPTION,
        "resume": RESUME,
        "job_requirements": None,
        "resume_profile": None,
        "fit_score": None,
        "skill_gaps": None,
        "strengths": None,
        "tailoring_advice": None,
        "upskilling_plan": None,
        "final_report": None
    }

    result = app.invoke(initial_state)

    print(result["final_report"])
    print(f"\nFit Score: {result['fit_score']}/100")
    print(f"Path taken: {'Strong fit' if result['fit_score'] >= 60 else 'Upskilling'}")