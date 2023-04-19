from django.db import models


class Questionnaire(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return f'[{self.id}] {self.title}'


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f'[{self.id}] {self.text}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()

    def __str__(self):
        return f'[{self.id}] {self.text}'


class QuestionsRelation(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='relations')
    from_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='from_relations', blank=True, null=True)
    from_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='to_relations')
