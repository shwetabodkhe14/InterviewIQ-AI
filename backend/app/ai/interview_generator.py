import json
from app.ai.gemini_client import client


class InterviewGenerator:

    @staticmethod
    def generate_questions(resume_data: dict):

        prompt = f"""
You are an expert Technical Interviewer.

The following is a parsed resume in JSON format.

{json.dumps(resume_data, indent=2)}

Generate interview questions based ONLY on this resume.

Return ONLY valid JSON.

{{
    "hr": [],
    "technical": [],
    "projects": []
}}

Rules:

- Generate exactly 5 HR questions.
- Generate exactly 10 Technical questions.
- Generate exactly 5 Project-based questions.
- Questions should become progressively harder.
- Do not include answers.
- Do not generate duplicate questions.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        return json.loads(response_text)