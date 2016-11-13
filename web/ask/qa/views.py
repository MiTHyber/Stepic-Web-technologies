from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qa.models import Question, Answer
from django.shortcuts import get_object_or_404
from qa.forms import AskForm, AnswerForm
from django.contrib.auth.models import User


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
    author = User.objects.get(username='Saya')
    if request.method == 'GET':
        q = get_object_or_404(Question, pk=pk)
        answers = Answer.objects.filter(question=q).all()
        form = AnswerForm()
        return render(request, 'question.html', {
            'question': q,
            'answers': answers,
            'form': form,
        })
    if request.method == 'POST':
        return answer(request)


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


def ask(request):
    author = User.objects.get(username='Saya')
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = author
            q = form.save()
            return HttpResponseRedirect(q.get_url())
    else:
        form = AskForm()
    return render(request, 'ask.html', {
        'form': form,
    })


def answer(request):
    author = User.objects.get(username='Saya')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = author
            form._question = request.POST.get('question')
            q = form.save()
            return HttpResponseRedirect(q.get_url())
