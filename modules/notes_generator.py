import os
from dotenv import load_dotenv
from groq import Groq
from modules.chatbot import retrieve_context

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_notes(task):

    context = retrieve_context(
        "important concepts summary definitions formulas topics",
        k=6
    )

    prompts = {

        "short_notes":
        """
Generate concise study notes.
""",

        "detailed_notes":
        """
Generate detailed notes with headings and explanations.
""",

        "important_points":
        """
Extract important points from the document.
""",

        "mcq":
        """
Generate 20 MCQs with answers.
""",

        "two_marks":
        """
Generate 20 two-mark questions with answers.
""",

        "five_marks":
        """
Generate 15 five-mark questions with answers.
""",

        "ten_marks":
        """
Generate 10 ten-mark questions with answers.
""",

        "flashcards":
        """
Generate flashcards in Question-Answer format.
""",

        "interview":
        """
Generate interview questions with answers.
""",

        "revision":
        """
Generate one-page revision sheet.
"""
    }

    prompt = f"""
You are StudyMate AI.

Task:
{prompts[task]}

Content:
{context}

Format output professionally.

Use:

# Main Heading

## Subheading

• Bullet Points

Important terms in bold.

Do not output plain text.
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