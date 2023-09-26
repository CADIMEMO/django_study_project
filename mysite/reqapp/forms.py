from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
class UserBioForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    age = forms.IntegerField(label='Age', min_value=1, max_value=120)
    bio = forms.CharField(label='Bio', widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile):
    if file.name and 'virus' in file.name:
        raise Exception('Файл не должен сожержать "virus"')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])

