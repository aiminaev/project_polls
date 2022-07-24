from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class Score(models.Model):
    score = models.IntegerField('Очки', default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Question(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField('Категория', blank=True, max_length=300)
    type = models.CharField('Тип', blank=True, max_length=300)
    difficulty = models.CharField('Трудность', blank=True, max_length=100)
    question = models.CharField('Вопрос', blank=True, max_length=500)
    correct_answer = models.CharField('Правильный ответ', blank=True, max_length=100)
    incorrect_answers = models.CharField('Неверный ответ', blank=True, max_length=1000)
