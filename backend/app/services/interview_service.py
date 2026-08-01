from app.ai.interview_generator import InterviewGenerator
from app.ai.answer_evaluator import AnswerEvaluator


class InterviewService:

    @staticmethod
    def generate_first_question(resume_data):

        questions = InterviewGenerator.generate_questions(
            resume_data
        )

        return questions[0]

    @staticmethod
    def evaluate(question, answer):

        return AnswerEvaluator.evaluate(
            question,
            answer
        )