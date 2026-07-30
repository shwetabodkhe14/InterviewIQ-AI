from app.ai.answer_evaluator import AnswerEvaluator

question = "Explain overfitting in Machine Learning."

answer = """
Overfitting happens when a machine learning model memorizes
the training data instead of learning the underlying patterns.
It performs well on training data but poorly on unseen data.
Cross-validation and regularization can help reduce overfitting.
"""

result = AnswerEvaluator.evaluate(
    question,
    answer
)

print(result)