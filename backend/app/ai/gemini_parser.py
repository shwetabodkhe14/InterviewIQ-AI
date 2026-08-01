import json

from google.genai import types
from app.ai.gemini_client import client


class GeminiParser:

    @staticmethod
    def extract_resume_data(text: str):

        prompt = f"""
You are an expert ATS Resume Parser.

Extract the resume into the following JSON.

{{
    "name":"",
    "email":"",
    "phone":"",
    "linkedin":"",
    "github":"",
    "summary":"",
    "skills":[],
    "education":[],
    "projects":[],
    "internships":[],
    "certifications":[],
    "achievements":[]
}}

Resume:

{text}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )

        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "")

        response_text = response_text.replace("```", "").strip()

        return json.loads(response_text)