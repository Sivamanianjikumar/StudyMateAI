import os
from dotenv import load_dotenv
from groq import Groq
from modules.chatbot import retrieve_context

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_research_response(task_type):
    context = retrieve_context("abstract introduction methodology results conclusion limitations future work", k=6)

    prompts = {
        "summary": """
Analyze this research paper and give:
1. Title
2. Abstract summary
3. Problem statement
4. Methodology
5. Results
6. Conclusion
""",
        "beginner": """
Explain this research paper like I am a complete beginner.
Use simple English and explain the purpose, method, and result clearly.
""",
        "focus": """
Tell the user how to read this research paper.
Explain:
1. Which sections to read first
2. What main points to focus on
3. What can be skipped initially
4. How to understand methodology
5. How to take notes from this paper
""",
        "gaps": """
Find research gaps in this paper.
Explain:
1. Limitations
2. Unsolved problems
3. Weaknesses
4. Future work mentioned
5. Possible improvements
""",
        "ideas": """
Suggest new research paper ideas based on this paper.
Give:
1. 5 possible new paper titles
2. Novelty for each idea
3. What improvement can be added
4. What experiments can be done
""",
        "writing": """
Guide the user to write another research paper based on this paper.
Explain:
1. Possible objective
2. Novelty to add
3. Dataset/experiment suggestions
4. Methodology structure
5. Paper section-wise writing plan
""",
        "viva": """
Generate presentation preparation content:
1. 2-minute explanation
2. 5-minute explanation
3. 10 viva questions with answers
4. Reviewer questions
"""
    }

    instruction = prompts.get(task_type, prompts["summary"])

    prompt = f"""
You are StudyMate AI Research Mentor.

Use the given paper context and generate a helpful research explanation.

Task:
{instruction}

Paper Context:
{context}

Use clear headings and simple English.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content