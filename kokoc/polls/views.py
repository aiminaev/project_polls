from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseServerError
from django.urls import reverse_lazy
import requests
from .models import Score, Question


def home(request):
    if request.user.is_authenticated:
        if not Score.objects.filter(user=request.user).exists():
            Score.objects.create(user=request.user)
        score = Score.objects.get(user=request.user)
        return render(request, 'polls/home.html', context={'score': score})
    return render(request, 'polls/home.html',)


@login_required
def test(request):
    print(request.method)
    if not Score.objects.filter(user=request.user).exists():
        Score.objects.create(user=request.user)
    score = Score.objects.get(user=request.user)
    current_score = score.score
    if request.method == 'POST':
        if not Question.objects.filter(user=request.user).exists():
            return redirect(reverse_lazy('polls:test'))
        question = get_object_or_404(Question, user=request.user)
        user_answer = request.POST.get('user_answer')
        if question.question != request.POST.get('question'):
            return redirect(reverse_lazy('polls:test'))
        if question.correct_answer == user_answer and question.question == request.POST.get('question'):
            current_score += 1
            score.score = current_score
            score.save()
        correct_answer = question.correct_answer
        text = question.question
        question.delete()
        return render(request, 'polls/test.html',
                      context={'correct_answer': correct_answer,
                               'results': [{'question': text}],
                               'score': score,
                               'is_answered': True,
                               }
                      )
    url = 'https://opentdb.com/api.php?amount=1&type=boolean'
    try:
        response = requests.get(url)
    except Exception as error:
        return HttpResponseServerError(error)
    if not response.status_code == 200:
        return HttpResponseServerError('Service not available. Please try again later')
    json = response.json()
    if not Question.objects.filter(user=request.user).exists():
        Question.objects.create(user=request.user)
    question = Question.objects.get(user=request.user)
    question.category = json['results'][0]['category']
    question.type = json['results'][0]['type']
    question.difficulty = json['results'][0]['difficulty']
    question.question = json['results'][0]['question']
    question.correct_answer = json['results'][0]['correct_answer']
    question.save()
    context = {'results': json['results'],
               'score': score,
               }

    return render(request, 'polls/test.html', context=context)