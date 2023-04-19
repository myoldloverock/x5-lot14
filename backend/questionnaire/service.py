from questionnaire.models import Question, Answer, QuestionsRelation, Questionnaire
from questionnaire.serializers import serialize_questionnaire


class QuestionnaireService:
    def get_questionnaire(self, questionnaire_id: int) -> dict:
        questionnaire = Questionnaire.objects.\
            prefetch_related('questions').\
            prefetch_related('questions__answers').\
            prefetch_related('relations').\
            get(id=questionnaire_id)
        return serialize_questionnaire(questionnaire)

    def create_question(self, questionnaire_id: int, text: str) -> int:
        question = Question(
            questionnaire_id=questionnaire_id,
            text=text,
        )
        question.save()
        return question.id

    def update_question(self, question_id: int, text: str):
        question = Question.objects.get(id=question_id)
        question.text = text
        question.save()

    def delete_question(self, question_id: int):
        question = Question.objects.get(id=question_id)
        question.delete()

    def create_answer(self, question_id: int, text: str) -> int:
        answer = Answer(
            question_id=question_id,
            text=text,
        )
        answer.save()
        return answer.id

    def update_answer(self, answer_id: int, text: str):
        answer = Answer.objects.get(id=answer_id)
        answer.text = text
        answer.save()

    def delete_answer(self, answer_id: int):
        answer = Answer.objects.get(id=answer_id)
        answer.delete()

    def create_relation(self, to_question_id: int, from_question_id: int, from_answer_id: int = None) -> int:
        to_question = Question.objects.get(id=to_question_id)
        relation = QuestionsRelation(
            questionnaire=to_question.questionnaire,
            to_question_id=to_question_id,
            from_question_id=from_question_id,
            from_answer_id=from_answer_id,
        )
        relation.save()
        return relation.id

    def update_relation(self, relation_id: int, update_data: dict):
        relation = QuestionsRelation.objects.get(id=relation_id)
        for key, value in update_data.items():
            setattr(relation, key, value)
        relation.save()

    def delete_relation(self, relation_id: int):
        relation = QuestionsRelation.objects.get(id=relation_id)
        relation.delete()
