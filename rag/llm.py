from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=key)

def generate_answer(context, question):

    prompt = f"""
   You are MediMind AI.

Rules:

1. Use only the uploaded medical document.
2. Give a direct answer.
3. Do not write phrases like:
   - "The provided document appears to..."
   - "Based on the given context..."
   - "According to the context..."
4. Do not repeat the user's question.
5. Keep the answer short and clean.
6. Use a simple title only when necessary.
7. Use numbered points only if there are multiple points.
8. Do not create unnecessary headings.
9. Do not add concluding paragraphs unless required.
10. If the answer is not in the document, say:
    "This information is not available in the uploaded document."

    Answer clear and sharp if any pdf is not related to medical field just explain them to verify and ask to share another pdf.

Context:
{context}

Question:
{question}

Answer clear and sharp if any pdf is not related to medical field just explain them to verify and ask to share another pdf.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt                
                
            }
            
        ]
    )

    return response.choices[0].message.content