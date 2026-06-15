import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_study_plan(subject, days, hours):

    prompt = f"""
You are an expert study planner.

Create a detailed study plan.

Subject: {subject}
Days Available: {days}
Hours Per Day: {hours}

Provide:

1. Day-wise schedule
2. Topics for each day
3. Revision plan
4. Mock test plan
5. Important tips

Use clean formatting.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content