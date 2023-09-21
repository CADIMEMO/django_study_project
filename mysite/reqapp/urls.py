from django.contrib import admin
from django.urls import path, include
from .views import process_get_view, user_form, handle_file_upload
app_name = 'reqapp'

urlpatterns = [
    path('', process_get_view, name='get_view'),
    path('forma/', user_form, name='user_form'),
    path('upload/', handle_file_upload, name='upload')

]
