from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from .forms import EmailPostForm, SearchForm
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

@login_required
def post_list(request, tag_slug = None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISHED,
        slug=post, publish__year=year,
        publish__month=month,
        publish__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in = post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags = Count('tags')
    ).order_by('-same_tags', 'publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    print(post.title)
    sent = False

    if request.method == "POST":

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} {cd['email']} recommends you read {post.title}"
            message = (f"Read {post.title} at {post_url} \n\n"
                       f"{cd['name']} comments: {cd['comments']}")
            send_mail(subject = subject, message = message, from_email=None, recipient_list= [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {"post": post, "form": form , "sent": sent})

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)

            results = (
                Post.published.annotate(
                    search=search_vector,
                    rank = SearchRank(search_vector, search_query)
                ).filter(search=query).order_by('-rank')
            )

    return render(request, 'blog/post/search.html',{
            'form': form,
            'query': query,
            'results': results
        })


class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def form_valid(self, form):

        return super().form_valid(form)

    def form_invalid(self, form):

        return self.render_to_response(self.get_context_data(form=form))


