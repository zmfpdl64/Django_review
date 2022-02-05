from django.db import models
from django.contrib.auth.models import User         #User db
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown



class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    #사람이 읽을 수 있는 텍스트로 url을 만들기위한 필드
    #allow_unicode=True로 한글 변환이 가능해진다.

    def __str__(self):  #관리자 페이지에서 사용하기 위한 함수
        return self.name

    class Meta:
        verbose_name_plural="Categories"    #class 사용하여 admin에 표기되는 카테고리 이름 변경
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'





class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   #urls에서 document의 기본경로를 세팅해놓았다.
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)  

    author = models.ForeignKey(User, on_delete=models.CASCADE) #user인 외래키와 연결해서 user가 삭제되면 같이 삭제된다.   
    #null=True //필드를 꼭 채우지 않아도 된다는 의미
    #on_delete=SET_NULL //작성자가 삭제되어도 Postdb는 삭제되지 않는다. 대신 작성자의 이름은 None으로 표기된다.
    category = models.ForeignKey(Category, blank=True ,null=True, on_delete=models.SET_NULL) #외래키를 설정하기 위해서는 이 클래스보다 앞에 선언해야한다.
    tag = models.ManyToManyField(Tag, blank=True)   #null은 None으로 저장

    def __str__(self):
        return f'[{self.pk}][{self.title}] :: {self.author}'   #Post객체가 호출되면 __str__함수가 실행되어 pk고유값과 title이 반환된다
                                            #[[self.pk][self.title]]이렇게 반환된다. f는 문자열 포맷팅이다. 관리자 페이지에서 자동으로 호출한다.
                                        
    def get_absolute_url(self):     #관리자 페이지( admin ) 에서 site에서 볼 수 있게 하는 함수
        return f'/blog/{self.pk}/'  #이 함수가 구현되어 있으면 관리자 페이지에서 버튼이 자동으로 생긴다.
    
    def get_content_markdown(self):
        return markdown(self.content)
    
    def get_file_name(self):
        #print(type(self.file_upload.name))  #string 형식
        #print(type(self.file_upload))       #django.db.models.fileds.FieldFile 형식
        return os.path.basename(str(self.file_upload)) #입력받은 file의 경로의 최하단 이름을 반환한다.
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #마지막 형식으로 파일의 형태를 구분한다.


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
