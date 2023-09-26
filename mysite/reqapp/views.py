import sys
from .forms import UserBioForm
from django.shortcuts import render
from django.http import HttpRequest
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
# Create your views here.
def process_get_view(request: HttpRequest):
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'result': result,
        'b': b,

    }
    return render(request, 'reqapp/request_query_params.html', context=context)


def user_form(request: HttpRequest):
    context = {
        'form': UserBioForm()
    }
    return render(request, 'reqapp/forma.html', context=context)

def handle_file_upload(request: HttpRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['my_file']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()

            filename = fs.save(myfile.name, myfile)

    else:
        form = UploadFileForm()
    context = {
        'form': form,
    }
    return render(request, 'reqapp/file-upload.html', context=context)