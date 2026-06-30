from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogCategory, BlogPost

def blog_home(request):
    posts_list = BlogPost.objects.all()
    categories = BlogCategory.objects.all()
    
    search_query = request.GET.get('search', '').strip()
    category_slug = request.GET.get('category', '').strip()
    
    # 1. Search filter
    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
        
    # 2. Category filter
    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)
        
    # 3. Identify featured post (only on first page when not filtering)
    featured_post = None
    if not search_query and not category_slug:
        featured_post = BlogPost.objects.filter(featured=True).first()
        if not featured_post:
            featured_post = BlogPost.objects.all().first()
            
        if featured_post:
            posts_list = posts_list.exclude(id=featured_post.id)
            
    # 4. Pagination
    paginator = Paginator(posts_list, 6) # 6 articles per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'featured_post': featured_post,
        'posts': posts,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Track view counts (simple increment)
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Fetch related articles (same category, max 3)
    related_posts = BlogPost.objects.filter(
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'blog/blog_detail.html', context)
