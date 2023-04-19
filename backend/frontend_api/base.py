import json

from django.http import HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from questionnaire.service import QuestionnaireService


@method_decorator(csrf_exempt, name='dispatch')
class BaseJSONView(View):
    service = QuestionnaireService()

    def parse_json_body(self, request: HttpRequest):
        body = request.body.decode('utf-8')
        return json.loads(body)

    def make_response(self, data: any):
        result = json.dumps(data)
        return HttpResponse(result, content_type='application/json')

