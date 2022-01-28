from django.shortcuts import redirect, render
from .models import Post, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

class PostList(ListView):
    model = Post    #자동으로 url에서 PostList를 호출하면 Post객체가 템플릿으로 전달된다.
    #ListView는 템플릿 이름을 설정 안할경우 기본적으로 index.html에 전달된다.
    #model이 index.html에 전달될때는 post_list로 전달된다.
    ordering = '-pk'
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category']  #model로 불러온 db의 사용할 속성을 필드에 담는다.

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostDetail(DetailView):
    model = Post    #템플릿 이름을 설정해주지 않으면 post_detail.html로 자동으로 연결된다.

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug != 'no_category':
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    else:
        category = '미분류'
        post_list = Post.objects.filter(category=None)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = Post.objects.filter(tag=tag)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
        }
    )
    