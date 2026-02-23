from django.db.models import Sum
from .models import postwalk, Comment
from .forms import CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WalkForm


# List all aproved walks
def walk_list(request):
    walks = postwalk.objects.filter(authorised=True)
    return render(request, 'walks/walk_list.html', {'walks': walks})


# Show one walk's details
def walk_detail(request, slug):
    walk = postwalk.objects.get(slug=slug)  # Get walk by slug
    comments = walk.comments.filter(authorised=True)  # Get all approved comments

    if request.method == 'POST':
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
    return render(request, 'index.html', {
        'featured_walks': featured_walks,
        'walk_count': walk_count,
        'total_distance': total_distance
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