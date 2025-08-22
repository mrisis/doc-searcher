from django import forms
from .models import Document
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام فایل را وارد کنید'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.doc'
            })
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # بررسی نوع فایل
            allowed_extensions = ['.pdf', '.docx', '.doc']
            file_extension = file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError("فقط فایل های PDF و Word پذیرفته می شود.")

            # بررسی حجم فایل (10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("حجم فایل نباید بیشتر از 10 مگابایت باشد.")

        return file


class SearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عبارت مورد نظر را وارد کنید...'
        }),
        label="عبارت جستجو"
    )

