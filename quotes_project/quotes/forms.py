from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    born_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter new tags separated by commas"
    )

    class Meta:
        model = Quote
        fields = ['quote', 'author']

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_tags = self.cleaned_data.get('new_tags', '')
        if commit:
            instance.save()
            if new_tags:
                tag_names = [tag.strip() for tag in new_tags.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
            self.save_m2m()
        return instance


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
