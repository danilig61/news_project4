from django import forms
from .models import Article, User, News
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content', 'author')

