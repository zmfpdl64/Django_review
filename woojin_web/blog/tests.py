from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
    
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        logo_btn = navbar.find('a', text='Woojin_Web') 
        self.assertEqual(logo_btn.attrs['href'],'/')   #attrs: 속성값 모두 출력이다. 여기서 

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        about_me_btn = navbar.find('a', text="About me")
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        

        

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
        #navbar = soup.find('nav') #1번
        #navbar = soup.nav                  #2번
        #1.5 Blog, About me 문구가 있다.
        self.navbar_test(soup)
        
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
    
    
    

