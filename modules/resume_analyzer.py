import os
from dotenv import load_dotenv
from groq import Groq
from modules.chatbot import retrieve_context

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume(task):

    context = retrieve_context(
        "resume skills projects education experience",
        k=6
    )

    prompts = {

        "ats": """
Give ATS score out of 100.
Explain score breakdown.
""",

        "skills": """
Extract technical skills, tools and technologies.
""",

        "missing": """
Identify missing skills for software engineering roles.
""",

        "strengths": """
List strengths of the resume.
""",

        "weaknesses": """
List weaknesses and areas of improvement.
""",

        "improve": """
Suggest detailed improvements for the resume.
""",

        "projects": """
Suggest 10 strong projects based on candidate profile.
""",

        "interview": """
Generate interview questions from resume.
""",

        "roles": """
Suggest suitable job roles based on resume.
"""
    }

    prompt = f"""
You are an expert resume reviewer.

Task:
{prompts[task]}

Resume:

{context}

Give clear formatting.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content