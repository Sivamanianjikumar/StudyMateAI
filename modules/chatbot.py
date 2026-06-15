import os
from dotenv import load_dotenv
from groq import Groq

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chunks = []
vectorizer = None
chunk_vectors = None


def create_chunks(text, chunk_size=800):
    text_chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            text_chunks.append(chunk)

    return text_chunks


def create_vector_store(text):
    global chunks, vectorizer, chunk_vectors

    chunks = create_chunks(text)

    vectorizer = TfidfVectorizer(stop_words="english")
    chunk_vectors = vectorizer.fit_transform(chunks)

    return len(chunks)


def retrieve_context(question, k=3):
    global chunks, vectorizer, chunk_vectors

    if chunk_vectors is None:
        return "No PDF uploaded yet."

    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, chunk_vectors).flatten()

    top_indices = similarities.argsort()[-k:][::-1]

    retrieved_chunks = []

    for idx in top_indices:
        retrieved_chunks.append(chunks[idx])

    return "\n\n".join(retrieved_chunks)


def generate_answer(question, mode="pdf"):
    context = retrieve_context(question)

    if mode == "pdf":
        prompt = f"""
You are StudyMate AI.

Answer the question only from the given PDF context.

PDF Context:
{context}

Question:
{question}

If answer is not found in PDF, say:
I could not find that information in the PDF.

Answer clearly.
"""
    else:
        prompt = f"""
You are StudyMate AI.

First use the PDF context. If the answer is not present in PDF, use general knowledge.

PDF Context:
{context}

Question:
{question}

Answer clearly.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content