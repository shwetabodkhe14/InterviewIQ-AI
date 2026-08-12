from google.genai import types
from app.ai.gemini_client import client

class ReportGenerator:

    @staticmethod
    def generate_overall_feedback(
        technical_score: int,
        communication_score: int,
        confidence_score: int,
        grammar_score: int,
        strengths: list,
        weaknesses: list
    ) -> dict:
        
        prompt = f"""
You are an expert technical interviewer and hiring manager. 
Based on the following candidate's mock interview performance data, generate a single overall AI feedback paragraph summarizing their performance. 
The summary should evaluate their technical ability, communication, confidence, grammar, biggest strengths, and biggest weaknesses. 
Finally, provide a clear hiring recommendation (e.g., "Recommended", "Not Recommended", "Needs Improvement").
Additionally, act as an AI Career Coach and provide a learning roadmap, recommended certifications, technologies, job roles, companies, and next steps for the candidate to improve their career trajectory based on this interview performance.

Data:
- Average Technical Score: {technical_score}/100
- Average Communication Score: {communication_score}/100
- Average Confidence Score: {confidence_score}/100
- Average Grammar Score: {grammar_score}/100
- Strengths: {', '.join(strengths)}
- Weaknesses: {', '.join(weaknesses)}

Return your response in the following JSON structure ONLY:
{{
    "overall_feedback": "Your comprehensive summary paragraph here...",
    "recommendation": "Your hiring recommendation here (e.g. Recommended, Not Recommended, Needs Improvement)",
    "learning_roadmap": ["Step 1...", "Step 2..."],
    "recommended_certifications": ["Cert 1...", "Cert 2..."],
    "recommended_technologies": ["Tech 1...", "Tech 2..."],
    "recommended_job_roles": ["Role 1...", "Role 2..."],
    "recommended_companies": ["Company 1...", "Company 2..."],
    "next_steps": ["Action 1...", "Action 2..."]
}}
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            import json
            
            text = response.text.strip()
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(text)
            return data
        except Exception as e:
            return {
                "overall_feedback": "Unable to generate AI feedback at this time.",
                "recommendation": "Unknown",
                "learning_roadmap": [],
                "recommended_certifications": [],
                "recommended_technologies": [],
                "recommended_job_roles": [],
                "recommended_companies": [],
                "next_steps": []
            }
