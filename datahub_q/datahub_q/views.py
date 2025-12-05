from django.shortcuts import render
from university.models import University

def index(request):
    universities = University.objects.all()
    return render(request, 'index.html', {'universities': universities})
