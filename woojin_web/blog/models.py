from django.db import models
import os

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   #urls에서 document의 기본경로를 세팅해놓았다.
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'[{self.pk}][{self.title}]'   #Post객체가 호출되면 __str__함수가 실행되어 pk고유값과 title이 반환된다
                                            #[[self.pk][self.title]]이렇게 반환된다. f는 문자열 포맷팅이다.
                                        
    def get_absolute_url(self):     #내부에서 정의되어있는 함수이다. 관리자 페이지( admin ) 에서 site에서 볼 수 있게 하는 함수
        return f'/blog/{self.pk}/'
    
    def get_file_name(self):
        #print(type(self.file_upload.name))  #string 형식
        #print(type(self.file_upload))       #django.db.models.fileds.FieldFile 형식
        return os.path.basename(str(self.file_upload)) #입력받은 file의 경로의 최하단 이름을 반환한다.
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #마지막 형식으로 파일의 형태를 구분한다.
