import json
from app.ai.gemini_client import client


class AnswerEvaluator:

    @staticmethod
    def evaluate(question: str, answer: str):

        prompt = f"""
You are a Senior Technical Interviewer.

Evaluate the candidate's answer.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON.

{{
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,
    "grammar_score": 0,
    "overall_score": 0,
    "strengths": [],
    "weaknesses": [],
    "feedback": ""
}}

Rules:
- Score each category out of 10.
- overall_score should be out of 100.
- Give constructive feedback.
- Never invent facts.
- Return only JSON.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "").strip()

        return json.loads(response_text)