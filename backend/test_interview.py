from app.ai.interview_generator import InterviewGenerator

resume_data = {
    "name": "Shweta Bodkhe",
    "skills": [
        "Python",
        "SQL",
        "Machine Learning",
        "FastAPI",
        "React",
        "Power BI"
    ],
    "projects": [
        "Virtual Doctor",
        "Foodie Vision"
    ]
}

questions = InterviewGenerator.generate_questions(
    resume_data
)

print(questions)