from django.contrib import admin

from questionnaire.models import Questionnaire, Question, Answer, QuestionsRelation

class QuestionnaireAdmin(admin.ModelAdmin):
    ...


class QuestionAdmin(admin.ModelAdmin):
    ...


class AnswerAdmin(admin.ModelAdmin):
    ...


class QuestionsRelationAdmin(admin.ModelAdmin):
    list_display = 'id', 'from_question', 'from_answer', 'to_question'






admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionsRelation, QuestionsRelationAdmin)
