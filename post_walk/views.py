from django.shortcuts import render
from django.http import HttpResponse
from .models import postwalk


# List all walks
def walk_list(request):
    walks = postwalk.objects.all()  # Get all walks from database
    return render(request, 'walks/walk_list.html', {'walks': walks})


# Show one walk's details
def walk_detail(request, pk):
    walk = postwalk.objects.get(pk=pk)  # Get walk by ID
    return render(request, 'walks/walk_detail.html', {'walk': walk})


# Home page
def index(request):
    return HttpResponse("Hello, world. You're at the post_walk index.")
