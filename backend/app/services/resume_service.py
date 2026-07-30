import os
import shutil
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.ats_scorer import ATSScorer
from app.ai.gemini_parser import GeminiParser
from app.parser.resume_parser import ResumeParser
from app.repositories.resume_repository import ResumeRepository

UPLOAD_FOLDER = "uploads/resumes"


class ResumeService:

    @staticmethod
    def upload_resume(
        db: Session,
        file: UploadFile,
        user_id: int
    ):

        print("Current Working Directory:", os.getcwd())

        upload_dir = os.path.abspath(UPLOAD_FOLDER)

        print("Upload Directory:", upload_dir)

        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)

        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are allowed.")

        # Generate unique filename
        unique_name = f"{uuid4()}_{file.filename}"

        filepath = os.path.join(upload_dir, unique_name)

        print("Saving to:", filepath)

        # Save PDF
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ====================================================
        # Extract Resume Text
        # ====================================================

        text = ResumeParser.extract_text(filepath)

        print("\n" + "=" * 80)
        print("📄 EXTRACTED RESUME TEXT")
        print("=" * 80)
        print(text)
        print("=" * 80)

        # ====================================================
        # AI Resume Parsing (Gemini)
        # ====================================================

        resume_data = GeminiParser.extract_resume_data(text)

        print("\n" + "=" * 80)
        print("🤖 AI STRUCTURED RESUME DATA")
        print("=" * 80)

        for key, value in resume_data.items():

            print(f"{key.upper()}:")

            if isinstance(value, list):

                if len(value) == 0:
                    print("  None")
                else:
                    for item in value:
                        print(f"  • {item}")

            else:
                print(f"  {value}")

            print()

        print("=" * 80)

        # ====================================================
        # ATS SCORE
        # ====================================================

        ats_result = ATSScorer.calculate(resume_data)

        print("\n" + "=" * 80)
        print("📊 ATS RESUME SCORE")
        print("=" * 80)

        print(f"Score : {ats_result['score']} / 100")
        print()

        print("Suggestions:")

        if ats_result["feedback"]:

            for item in ats_result["feedback"]:
                print(f"• {item}")

        else:
            print("Excellent Resume! No major improvements required.")

        print("=" * 80 + "\n")

        # ====================================================
        # Save Resume Metadata
        # ====================================================

        saved_resume = ResumeRepository.create(
            db=db,
            filename=file.filename,
            filepath=filepath,
            user_id=user_id
        )

        return saved_resume