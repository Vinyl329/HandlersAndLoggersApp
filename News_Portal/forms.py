from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=50)
    class Meta:
        model = Post
        fields = [
            'statement',
            'type',
            'category',
            'text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        statement = cleaned_data.get("statement")
        text = cleaned_data.get("text")

        if statement == text:
            raise ValidationError(
                "Заголовок не должен быть идентичен тексту."
            )

        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user