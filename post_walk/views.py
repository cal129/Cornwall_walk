from django.db.models import Sum
from django.shortcuts import render
from .models import postwalk


# List all walks
def walk_list(request):
    walks = postwalk.objects.all()  # Get all walks from database
    return render(request, 'walks/walk_list.html', {'walks': walks})


# Show one walk's details
def walk_detail(request, slug):
    walk = postwalk.objects.get(slug=slug)  # Get walk by slug
    return render(request, 'walks/walk_detail.html', {'walk': walk})


# Home page
def index(request):
    featured_walks = postwalk.objects.filter(featured=True).order_by('-date_added')[:3]
    walk_count = postwalk.objects.count()  # Counts total walks
    total_distance = postwalk.objects.aggregate(Sum('distance'))['distance__sum'] or 0  # Sums all distances
    return render(request, 'index.html', {
        'featured_walks': featured_walks,
        'walk_count': walk_count,
        'total_distance': total_distance
    })
