from django import forms
from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=50)
    text = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args,**kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField()
    question = forms.ModelChoiceField(queryset=Question.objects.all())

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args,**kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        return Answer.objects.create(**self.cleaned_data)
