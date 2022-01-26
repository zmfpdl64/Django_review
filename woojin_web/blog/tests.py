from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        #1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        #1.2 정상적으로 페이지가 로드된다. 
        self.assertEqual(response.status_code, 200)
        #1.3 페이지 타이틀은 Blog다
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(type(response))
        #print(response.content)
        #print(type(soup))
        #print(soup)
        self.assertEqual(soup.title.text, 'Blog')
        #1.4 내비게이션 바가 있다.
        navbar = soup.find('nav') #1번
        #navbar = soup.nav                  #2번
        #1.5 Blog, About me 문구가 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)
        
        # 2.1 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        #2.2 아직 게시물이 없습니다. 라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        print(type(main_area), type(main_area.text))    #bs4.element.Tag 형태이고 text를 붙히면 str형태로 바뀐다.

        #3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content = 'First',            
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content = 'Second',            
        )
        self.assertEqual(Post.objects.count(), 2)

        #3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        #3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        #3.4 '아직 게시물이 없습니다.'라는 문구가 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area)
    
    def test_post_detail(self):
        #1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title = "첫 번째 포스터입니다.",
            content = "first",

        )
        self.assertEqual(Post.objects.count(), 1)
        #1.2 그 포스트의 url은 '/blog/1/'이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')
        
        #2. 첫 번째 포스트의 상세 페이지 테스트
        #2.1. 첫번째 프스트의 url로 접근하여 정상적인지 확인
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        #2.2 포스트의 네비게이션 바가 있는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)
        #2.3 웹 브라우저 탭 타이틀에 타이틀이 들어있나
        self.assertIn(post_001.title, soup.title.text )
        #2.4 첫 번째 포스트의 제목이 들어있나
        main_area = soup.find('div', id='post-area')
        self.assertIn(post_001.title, main_area.text)
        #2.5 첫 번째 포스트에 작성자명이 들어있나

        #2.6 첫 번째 포스트의 내용이 포스트영역에 있나
        self.assertIn(post_001.content, main_area.text)

