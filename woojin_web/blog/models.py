from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'[{self.pk}][{self.title}]'   #Post객체가 호출되면 __str__함수가 실행되어 pk고유값과 title이 반환된다
                                            #[[self.pk][self.title]]이렇게 반환된다. f는 문자열 포맷팅이다.
