from django.db.models import Sum
from .models import postwalk, Comment
from .forms import CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WalkForm
from django.core.paginator import Paginator
import json
import re


def parse_coordinates(coord_string):
    """
    Parse coordinate string like '49.9250° N, 6.2987° W' into (lat, lng).
    Returns None if parsing fails.
    """
    try:
        pattern = r'([\d.]+)°\s*([NS]),\s*([\d.]+)°\s*([EW])'
        match = re.match(pattern, coord_string.strip())
        if not match:
            return None
        lat_val, lat_dir, lng_val, lng_dir = match.groups()
        lat = float(lat_val) * (1 if lat_dir == 'N' else -1)
        lng = float(lng_val) * (1 if lng_dir == 'E' else -1)
        return (lat, lng)
    except (ValueError, AttributeError):
        return None


# List all aproved walks
def walk_list(request):
    sort = request.GET.get('sort', 'oldest')
    sort_map = {
        'newest': ['-date_added'],
        'oldest': ['date_added'],
        'distance_asc': ['distance', 'title'],
        'distance_desc': ['-distance', 'title'],
        'duration_asc': ['time_hours', 'time_minutes', 'title'],
        'duration_desc': ['-time_hours', '-time_minutes', 'title'],
        'type': ['type', 'title'],
    }
    order_by_fields = sort_map.get(sort, sort_map['newest'])
    walks_list = postwalk.objects.filter(authorised=True).order_by(*order_by_fields)
    paginator = Paginator(walks_list, 6)  # 6 walks per page
    page_number = request.GET.get('page')
    walks = paginator.get_page(page_number)
    return render(request, 'walks/walk_list.html', {'walks': walks, 'sort': sort})


# Show one walk's details
def walk_detail(request, slug):
    walk = postwalk.objects.get(slug=slug)
    comments = walk.comments.filter(approved=True)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.walk = walk
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('walk_detail', slug=slug)
    else:
        comment_form = CommentForm()

    return render(request, 'walks/walk_detail.html', {
        'walk': walk,
        'comments': comments,
        'comment_form': comment_form
    })


# Home page
def index(request):
    featured_walks = postwalk.objects.filter(featured=True, authorised=True).order_by('-date_added')[:3]
    walk_count = postwalk.objects.filter(authorised=True).count()  # Counts only approved walks
    total_distance = postwalk.objects.filter(authorised=True).aggregate(Sum('distance'))['distance__sum'] or 0  # Sums only approved walks

    # Gather all authorised walks with coordinates for the map
    all_walks = postwalk.objects.filter(authorised=True)
    walk_markers = []
    for walk in all_walks:
        coords = parse_coordinates(walk.coordinates)
        if coords:
            walk_markers.append({
                'title': walk.title,
                'lat': coords[0],
                'lng': coords[1],
                'slug': walk.slug,
                'location': walk.location
            })

    return render(request, 'index.html', {
        'featured_walks': featured_walks,
        'walk_count': walk_count,
        'total_distance': total_distance,
        'walk_markers': json.dumps(walk_markers)
    })


# Delete a comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only allow the comment owner to delete it
    if request.user == comment.user:
        walk_slug = comment.walk.slug
        comment.delete()
        messages.success(request, 'Your comment has been deleted.')
        return redirect('walk_detail', slug=walk_slug)
    else:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('walk_detail', slug=comment.walk.slug)


# Post a walk - only if logged in.
@login_required
def walk_create(request):
    if request.method == 'POST':
        form = WalkForm(request.POST, request.FILES)
        if form.is_valid():
            walk = form.save(commit=False)
            walk.user = request.user
            walk.slug = slugify(walk.title)
            walk.save()
            messages.success(request, 'Your walk has been submitted and is awaiting approval!')
            return redirect('walk_list')
    else:
        form = WalkForm()
    return render(request, 'walks/walk_form.html', {'form': form})


# Edit a comment - only if logged in and owns the comment.
@login_required
def comment_edit(request, comment_id):
    """View to edit a comment"""
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if user owns the comment
    if comment.user != request.user:
        messages.error(request, "You can only edit your own comments.")
        return redirect('walk_detail', slug=comment.walk.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = False  # Set to not approved
            comment.edited = True     # Mark as edited
            comment.save()
            messages.success(request, "Comment updated! It will be visible once approved by an admin.")
            return redirect('walk_detail', slug=comment.walk.slug)

    return redirect('walk_detail', slug=comment.walk.slug)


# View to display user's favourite walks
@login_required
def favourite_walks(request):
    """View to display user's favourite walks"""
    walks = request.user.favourite_walks.filter(authorised=True).order_by('-date_added')
    return render(request, 'walks/favourite_walks.html', {'walks': walks})


@login_required
def toggle_favourite(request, slug):
    """Toggle a walk as favourite"""
    walk = get_object_or_404(postwalk, slug=slug)

    if walk in request.user.favourite_walks.all():
        request.user.favourite_walks.remove(walk)
        messages.success(request, f'Removed {walk.title} from favourites.')
    else:
        request.user.favourite_walks.add(walk)
        messages.success(request, f'Added {walk.title} to favourites!')

    return redirect('walk_detail', slug=slug)
