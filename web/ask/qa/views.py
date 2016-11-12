from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qa.models import Question, Answer
from django.shortcuts import get_object_or_404


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def recent_questions(request):
    questions = Question.objects.new().all()
    paginator = Paginator(questions, 10)
    paginator.baseurl = '/?page='
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'questions_list.html', {
        'questions': questions.object_list,
        'paginator': paginator,
        'page': page,
    })


def question(request, pk):
    q = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=q).all()
    return render(request, 'question.html', {
        'question': q,
        'answers': answers,
    })


def popular_questions(request):
    questions = Question.objects.popular().all()
    paginator = Paginator(questions, 10)
    paginator.baseurl = '/popular/?page='
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'questions_list.html', {
        'questions': questions.object_list,
        'paginator': paginator,
        'page': page,
    })