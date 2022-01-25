from .models import Post
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post    #자동으로 url에서 PostList를 호출하면 Post객체가 템플릿으로 전달된다.
    #ListView는 템플릿 이름을 설정 안할경우 기본적으로 index.html에 전달된다.
    #model이 index.html에 전달될때는 post_list로 전달된다.
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post    #템플릿 이름을 설정해주지 않으면 post_detail.html로 자동으로 연결된다.


