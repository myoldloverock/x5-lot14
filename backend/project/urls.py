from django.contrib import admin
from django.urls import path

from frontend_api.views import GetQuestionnaire, CreateQuestion, UpdateQuestion, DeleteQuestion, CreateAnswer, \
    UpdateAnswer, DeleteAnswer, CreateRelation, UpdateRelation, DeleteRelation

urlpatterns = [
    path('admin/', admin.site.urls),

    path('frontend_api/get_questionnaire/<int:questionnaire_id>/', GetQuestionnaire.as_view(), name='get_questionnaire'),
    path('frontend_api/create_question/', CreateQuestion.as_view(), name='create_question'),
    path('frontend_api/update_question/', UpdateQuestion.as_view(), name='update_question'),
    path('frontend_api/delete_question/', DeleteQuestion.as_view(), name='delete_question'),
    path('frontend_api/create_answer/', CreateAnswer.as_view(), name='create_answer'),
    path('frontend_api/update_answer/', UpdateAnswer.as_view(), name='update_answer'),
    path('frontend_api/delete_answer/', DeleteAnswer.as_view(), name='delete_answer'),
    path('frontend_api/create_relation/', CreateRelation.as_view(), name='create_relation'),
    path('frontend_api/update_relation/', UpdateRelation.as_view(), name='update_relation'),
    path('frontend_api/delete_relation/', DeleteRelation.as_view(), name='delete_relation'),
]
