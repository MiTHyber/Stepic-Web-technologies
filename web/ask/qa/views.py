from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qa.models import Question, Answer
from django.shortcuts import get_object_or_404
from qa.forms import AskForm, AnswerForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
    if request.method == 'GET':
        form = AnswerForm()
        return render(request, 'question.html', {
            'question': q,
            'answers': answers,
            'form': form,
        })
    if request.method == 'POST':
        Answer.objects.create(text=request.POST.get('text'),question=q,author=request.user)
        form = AnswerForm
        return render(request, 'question.html', {
            'question': q,
            'answers': answers,
            'form': form,
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


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            q = form.save()
            return HttpResponseRedirect(q.get_url())
    else:
        form = AskForm()
    return render(request, 'ask.html', {
        'form': form,
    })


def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            form._question = request.POST.get('question')
            q = form.save()
            return HttpResponseRedirect(q.get_url())


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            q = form.save()
            login(request, q)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {
        'form': form,
    })
