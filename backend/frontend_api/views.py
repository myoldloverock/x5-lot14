from django.http import HttpRequest, HttpResponse

from frontend_api.base import BaseJSONView



class GetQuestionnaire(BaseJSONView):
    def get(self, request: HttpRequest, questionnaire_id: int) -> HttpResponse:
        questionnaire = self.service.get_questionnaire(questionnaire_id)
        return self.make_response(questionnaire)


class CreateQuestion(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        questionnaire_id, text = body['questionnaire_id'], body['text']
        question_id = self.service.create_question(questionnaire_id, text)
        return self.make_response(question_id)


class UpdateQuestion(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        question_id, text = body['question_id'], body['text']
        self.service.update_question(question_id, text)
        return self.make_response({'ok': True})


class DeleteQuestion(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        question_id = body['question_id']
        self.service.delete_question(question_id)
        return self.make_response({'ok': True})


class CreateAnswer(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        question_id, text = body['question_id'], body['text']
        answer_id = self.service.create_answer(question_id, text)
        return self.make_response(answer_id)


class UpdateAnswer(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        answer_id, text = body['answer_id'], body['text']
        self.service.update_answer(answer_id, text)
        return self.make_response({'ok': True})


class DeleteAnswer(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        answer_id = body['answer_id']
        self.service.delete_answer(answer_id)
        return self.make_response({'ok': True})


class CreateRelation(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        to_question_id, from_question_id, from_answer_id = \
            body['to_question_id'], body['from_question_id'], body['from_answer_id']
        relation_id = self.service.create_relation(to_question_id, from_question_id, from_answer_id)
        return self.make_response(relation_id)


class UpdateRelation(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        relation_id, update_data = body['relation_id'], body['update_data']
        self.service.update_relation(relation_id, update_data)
        return self.make_response({'ok': True})


class DeleteRelation(BaseJSONView):
    def post(self, request: HttpRequest) -> HttpResponse:
        body = self.parse_json_body(request)
        relation_id = body['relation_id']
        self.service.delete_relation(relation_id)
        return self.make_response({'ok': True})
