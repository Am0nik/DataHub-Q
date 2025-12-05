from django.shortcuts import render
from django.shortcuts import get_object_or_404
from university.models import University
# Create your views here.

def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    return render(request, 'university_detail.html', {'university': university})