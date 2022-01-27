from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

admin.site.register(Post)
#admin.site.register(Category)  이렇게 선언해도 되지만 네임을 입력했을 때 자동으로 slug필드까지 채워주기 위해 class를 선언하겠다.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin) #첫번째 인자에 테이블 집어넣고 두번째 인자에 실행될 클래스를 집어넣었다.

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Tag, TagAdmin)