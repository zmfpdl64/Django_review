from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk') #속성을 리버스로 하여 posts에 저장한다.
    return render(
        request,    #여기서 request는 사용가 post형식으로 보냈을때의 form데이터를 저장한다.

        'blog/index.html',
        {
            'posts': posts,
        },
    )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post':post,
        }
    )