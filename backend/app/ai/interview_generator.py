import json
import re
import logging
from typing import Dict, Any, List

from google.genai import types
from app.ai.gemini_client import client

logger = logging.getLogger(__name__)

class InterviewGenerator:

    @staticmethod
    def _clean_json_string(raw_text: str) -> str:
        """
        Extracts JSON from text, removes markdown, and applies heuristics to fix common JSON errors.
        """
        text = raw_text.strip()
        
        # Extract only the JSON block if extra text exists
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            text = text[start:end+1]

        # Remove trailing commas
        text = re.sub(r",(\s*[}\]])", r"\1", text)
        
        # Clean up any potential markdown left over
        text = text.replace("```json", "")
        text = text.replace("```", "")
        
        return text.strip()

    @staticmethod
    def _validate_structure(data: Dict[str, Any]) -> bool:
        """
        Validates the parsed JSON to ensure it has the correct structure and counts.
        """
        required_keys = {"hr", "technical", "projects"}
        if not required_keys.issubset(data.keys()):
            return False
            
        if not isinstance(data.get("hr"), list) or len(data["hr"]) != 5:
            return False
            
        if not isinstance(data.get("technical"), list) or len(data["technical"]) != 10:
            return False
            
        if not isinstance(data.get("projects"), list) or len(data["projects"]) != 5:
            return False
            
        return True

    @staticmethod
    def generate_questions(resume_data: dict) -> Dict[str, List[str]]:
        prompt = f"""
You are an expert Technical Interviewer.

Below is a candidate's parsed resume in JSON format.

{json.dumps(resume_data, indent=2)}

Generate personalized interview questions ONLY from the candidate's resume.

Rules:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT wrap inside ```.
- You must generate EXACTLY 5 HR questions.
- You must generate EXACTLY 10 Technical questions.
- You must generate EXACTLY 5 Projects questions.
- Ensure all quotes inside strings are properly escaped.
- Ensure no trailing commas in arrays.

Return exactly in this format:
{{
  "hr": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ],
  "technical": [
    "...",
    "...",
    "...",
    "...",
    "...",
    "...",
    "...",
    "...",
    "...",
    "..."
  ],
  "projects": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ]
}}
"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    ),
                )
                
                if not response or not response.text:
                    continue

                cleaned_text = InterviewGenerator._clean_json_string(response.text)
                
                # Attempt to parse JSON. strict=False allows unescaped control chars like newlines
                try:
                    data = json.loads(cleaned_text, strict=False)
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parsing failed on attempt {attempt + 1}: {e}")
                    # Attempt a rudimentary fix for unescaped newlines/tabs inside strings if needed
                    # By replacing literal newlines with spaces, we might save the JSON
                    fixed_text = cleaned_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    try:
                        data = json.loads(fixed_text, strict=False)
                    except json.JSONDecodeError:
                        continue # Move to next retry
                
                # Validate structure
                if InterviewGenerator._validate_structure(data):
                    return data
                else:
                    logger.warning(f"JSON structure/counts invalid on attempt {attempt + 1}")

            except Exception as e:
                logger.error(f"Error calling Gemini on attempt {attempt + 1}: {e}")
                
        raise ValueError("Failed to generate valid interview questions with correct counts after 3 attempts.")