import re


class InformationExtractor:

    @staticmethod
    def extract(text: str):

        data = {}

        # Split resume into lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # =========================
        # Name
        # =========================
        data["name"] = lines[0] if lines else ""

        # =========================
        # Email
        # =========================
        email = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        data["email"] = email.group() if email else ""

        # =========================
        # Phone
        # =========================
        phone = re.search(
            r"(\+91[\s-]?)?[6-9]\d{9}",
            text
        )

        data["phone"] = phone.group() if phone else ""

        # =========================
        # LinkedIn
        # =========================
        linkedin = re.search(
            r"(https?://)?(www\.)?linkedin\.com/[^\s]+",
            text,
            re.IGNORECASE
        )

        data["linkedin"] = linkedin.group() if linkedin else ""

        # =========================
        # GitHub
        # =========================
        github = re.search(
            r"(https?://)?(www\.)?github\.com/[^\s]+",
            text,
            re.IGNORECASE
        )

        data["github"] = github.group() if github else ""

        # =========================
        # Skills
        # =========================

        skill_list = [
            "Python","Java","C","C++","SQL","Machine Learning",
            "Deep Learning","Artificial Intelligence","AI","NLP",
            "FastAPI","Flask","Django","React","Node.js",
            "HTML","CSS","JavaScript","Power BI","Excel",
            "Pandas","NumPy","Scikit-learn","TensorFlow",
            "PyTorch","Git","GitHub","MySQL","Firebase",
            "Docker","Linux","MongoDB","PostgreSQL"
        ]

        found_skills = []

        lower_text = text.lower()

        for skill in skill_list:

            if skill.lower() in lower_text:
                found_skills.append(skill)

        data["skills"] = sorted(set(found_skills))

        # =========================
        # Generic Section Extractor
        # =========================

        def extract_section(start_keywords, end_keywords):

            capture = False
            section = []

            for line in lines:

                lower = line.lower()

                if any(k in lower for k in start_keywords):
                    capture = True
                    continue

                if capture and any(k in lower for k in end_keywords):
                    break

                if capture:
                    section.append(line)

            return section

        # =========================
        # Summary
        # =========================

        data["summary"] = extract_section(
            ["professional summary", "summary", "profile"],
            ["technical skills", "skills", "education"]
        )

        # =========================
        # Education
        # =========================

        data["education"] = extract_section(
            ["education"],
            ["projects", "internship", "experience", "certification", "achievements", "languages"]
        )

        # =========================
        # Projects
        # =========================

        data["projects"] = extract_section(
            ["projects"],
            ["internship", "experience", "certification", "achievements", "languages"]
        )

        # =========================
        # Internship
        # =========================

        data["internships"] = extract_section(
            ["internship", "experience"],
            ["certification", "achievements", "languages"]
        )

        # =========================
        # Certifications
        # =========================

        data["certifications"] = extract_section(
            ["certifications", "certification"],
            ["achievements", "languages"]
        )

        # =========================
        # Achievements
        # =========================

        data["achievements"] = extract_section(
            ["achievements"],
            ["languages"]
        )

        # =========================
        # Languages
        # =========================

        data["languages"] = extract_section(
            ["languages"],
            []
        )

        return data