from django.shortcuts import redirect, render
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify 
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


class PostList(ListView):
    model = Post    #자동으로 url에서 PostList를 호출하면 Post객체가 템플릿으로 전달된다.
    #ListView는 템플릿 이름을 설정 안할경우 기본적으로 index.html에 전달된다.
    #model이 index.html에 전달될때는 post_list로 전달된다.
    ordering = '-pk'
    paginate_by = 5

    #def dispatch(self, request, *args, **kwargs):
    #    post_list = Post.objects.all()
    #    page = request.GET.get('page', '1')
    #    paginator = Paginator(post_list, '5')
    #    page_obj = paginator.page(page)
    #    return 
    
    def get_context_data(self, **kwargs):   #Post 모델을 포함하여 추가적으로 더 보내고 싶은 keywards가 있으면 추가하는 함수이다.
        #post_list = Post.objects.all()
        #paginator = Paginator(post_list, 5)
        #page = self.GET.get('page')
        #posts = paginator.get_page(page)
        context = super(PostList, self).get_context_data()
        #context['page'] = posts
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category']  #model로 불러온 db의 사용할 속성을 필드에 담는다.
    #user라는 필드는 없지만 user db는 기본적으로 항상 전달된다.?
    #PostCreate에서는 기본적으로 fields에 속성을 담으면 form이라는 변수에 담아서 전달한다.
    def form_valid(self, form): #post일 때 실행한다.
        current_user = self.request.user
        #for i in self.fields('title'):
        #    print(i)
        #self라고 하면 그 class를 의미한다.
        #print(form.instance.author) #새로운 인스턴스를 생성하
        #print(form) #html형식의 입력값들을 의미한다.
        #print(self) #<blog.views.PostCreate object at 0x052720B8>
        #print(self.request.user, self.request.POST.get('author'))  #self.request.POST.author 속성을 갖고있지 않음 form.author 도 속성을 갖고있지 않음
        #self.request.POST는 딕셔너리형이기에 속성의 이름으로 value를 확인할 수 있다.
        #print(self.request)
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user #입력값에는 작성자가 없기 때문에 인스턴스 변수를 추가하여 현재의 작성자를 추가한다.
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            print(tags_str)
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    print(t)
                    
                    ntag, is_tag_created = Tag.objects.get_or_create(name=t)    #db에서 오류가 공백을 저장하여 오류가 발생하였다.
                    
                    if is_tag_created:
                        ntag.slug = slugify(t, allow_unicode=True)
                        ntag.save()
                    self.object.tag.add(ntag)
            return response    
        else:
            return redirect('/blog/')        
            




class PostUpdate(LoginRequiredMixin, UpdateView):   #UpdateView 클래스를 상속받아서 하기 때문에 
    model = Post
    fields = ['title', 'content', 'head_image','file_upload', 'category']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tag.exists():
            tags_str_list = list()
            for t in self.object.tag.all():
                tags_str_list.append(t.name) #t에는 slug, name 속성이 있다.
            context['tags_str_default'] = '; '.join(tags_str_list) #join은 리스트를 문자열로 변환시키는 함수이다.
        
        return context

    def dispatch(self, request, *args, **kwargs):   #dispatch 메서드에서 get, post 메서드를 알아낸다.
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def form_valid(self, form): #post일 때 실행한다.
        response = super(PostUpdate, self).form_valid(form)
        self.object.tag.clear() #db와의 관계를 해제한다.
        tags_str = self.request.POST.get('tags_str')
        print(tags_str)
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')

            if tags_str[-1] == ';':
                tags_str = tags_str[:-1]
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t) #사용자가 작성한 tag를 db의 name과 비교하여 있으면 생성하지않고 없으면 생성한다.
                #tag는 새로 생성한 레코드, is_tag_created는 생성이 되었는가 여부 True, False
                #name 속성은 자동으로 채워진다. tag.name == " "
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True) #slugify로 
                    tag.save()  #db에 저장한다.
                self.object.tag.add(tag)    #전송했던 포스트의 태그필드에 추가하는 코드
        
        return response


class PostDetail(DetailView):
    model = Post    #템플릿 이름을 설정해주지 않으면 post_detail.html로 자동으로 연결된다.

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        #context['comment_set'] = Comment.objects.filter(post = self.pk)
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
    #print(request)#<WSGIRequest: GET '/blog/tag/%EC%9A%B0%EC%A7%84%EC%9E%A5%EA%B3%A0/'>  get_absolute_url 로 뒤에 암호문은 slug값이다.
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
        }
    )
    
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)    # comment = get_object_or_404(Comment, pk=pk) 이 메소드를 사용하여 불러올수도 있다.
    post = comment.post
    #print('i am ',comment.content)
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    raise PermissionDenied
