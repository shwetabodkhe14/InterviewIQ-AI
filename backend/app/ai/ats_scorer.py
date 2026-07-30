class ATSScorer:

    @staticmethod
    def calculate(resume_data):

        score = 0

        feedback = []

        # -----------------------
        # Contact Information
        # -----------------------

        if resume_data.get("email"):
            score += 10
        else:
            feedback.append("Add a professional email address.")

        if resume_data.get("phone"):
            score += 5
        else:
            feedback.append("Add your phone number.")

        if resume_data.get("linkedin"):
            score += 5
        else:
            feedback.append("Add your LinkedIn profile.")

        if resume_data.get("github"):
            score += 5
        else:
            feedback.append("Add your GitHub profile.")

        # -----------------------
        # Summary
        # -----------------------

        if len(resume_data.get("summary", [])) > 0:
            score += 10
        else:
            feedback.append("Add a professional summary.")

        # -----------------------
        # Skills
        # -----------------------

        skills = resume_data.get("skills", [])

        if len(skills) >= 10:
            score += 20

        elif len(skills) >= 5:
            score += 10

        else:
            feedback.append("Include more technical skills.")

        # -----------------------
        # Projects
        # -----------------------

        projects = resume_data.get("projects", [])

        if len(projects) > 0:
            score += 15
        else:
            feedback.append("Add projects.")

        # -----------------------
        # Education
        # -----------------------

        education = resume_data.get("education", [])

        if len(education) > 0:
            score += 10
        else:
            feedback.append("Education section missing.")

        # -----------------------
        # Internship
        # -----------------------

        internships = resume_data.get("internships", [])

        if len(internships) > 0:
            score += 10

        # -----------------------
        # Certifications
        # -----------------------

        certs = resume_data.get("certifications", [])

        if len(certs) > 0:
            score += 5

        # -----------------------
        # Achievements
        # -----------------------

        achievements = resume_data.get("achievements", [])

        if len(achievements) > 0:
            score += 5

        return {
            "score": score,
            "feedback": feedback
        }