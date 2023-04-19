from questionnaire.models import Questionnaire


def serialize_questionnaire(questionnaire: Questionnaire) -> dict:
    return {
        'id': questionnaire.id,
        'questions': [
            {
                'id': question.id,
                'text': question.text,
                'answers': [
                    {
                        'id': answer.id,
                        'text': answer.text,
                    }
                    for answer in question.answers.all()
                ]
            } for question in questionnaire.questions.all()
        ],
        'relations': [
            {
                'id': relation.id,
                'from_question_id': relation.from_question.id if relation.from_question else None,
                'from_answer_id': relation.from_answer.id if relation.from_answer else None,
                'to_question_id': relation.to_question.id,
            }
            for relation in questionnaire.relations.all()
        ]
    }
