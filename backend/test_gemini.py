from app.ai.gemini_parser import GeminiParser

result = GeminiParser.extract_resume_data("""
My name is Shweta Bodkhe.

Email: shwetabodkhe@gmail.com


Skills:
Python
SQL
Machine Learning

Projects:
Virtual Doctor
Foodie Vision
""")

print(result)