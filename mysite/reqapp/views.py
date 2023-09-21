import sys

from django.shortcuts import render
from django.http import HttpRequest
from django.core.files.storage import FileSystemStorage
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
    return render(request, 'reqapp/forma.html')

def handle_file_upload(request: HttpRequest):
    if request.method == 'POST' and request.FILES.get('my_file'):
        myfile = request.FILES['my_file']
        fs = FileSystemStorage()
        if fs.size(myfile.name) < 1000000:
            filename = fs.save(myfile.name, myfile)
        else:
            raise Exception

    return render(request, 'reqapp/file-upload.html')