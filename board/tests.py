from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Board', navbar.text)
        self.assertIn('Maps', navbar.text)

    def test_post_list(self):
        # 1.1. 포스트 목록 페이지 가져온다.
        response = self.client.get('/board/')

        # 1.2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        # 1.3. 페이지 타이틀은 'Board' 이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Board')

        self.navbar_test(soup)

        # 2.1. 포스트(게시물)가 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)

        # 2.2. main area 에 '아직 게시물이 없습니다' 라는 문구가 나타난다.
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        # 3.1. 포스트가 2개 있다면
        post_001 = Post.objects.create(title = '첫 번째 포스트입니다.', content = 'Hello World. We are the world.',)
        post_002 = Post.objects.create(title = '두 번째 포스트입니다.', content = '1등이 전부는 아니잖아요?',)
        self.assertEqual(Post.objects.count(), 2)

        # 3.2. 포스트 목록 페이지를 새로고침했을때
        response = self.client.get('/board/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # 3.3. main area 에 포스트 2개의 제목이 존재한다.
        main_area = soup.find('div', id = 'main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3.4. '아직 게시물이 없습니다' 라는 문구는 더 이상 나타나지 않는다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)


    def test_post_detail(self):
        # 1.1. Post가 하나 있다.
        post_001 = Post.objects.create(title = '첫 번째 포스트입니다.', content = 'Hello World. We are the world',)

        # 1.2. 그 포스트의 url은 'board/1/' 이다.
        self.assertEqual(post_001.get_absoulte_url(), '/Board/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 post url로 접근하면 정상적으로 작동한다 (status code : 200).
        response = self.client.get(post_001.get_absoulte_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)

        # 2.3. 첫 번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2.4. 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area = soup.find('div', id = 'main = area')
        post_area = main.area.find('div', id = 'post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2.5. 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        # 아적 미작성

        # 2.6. 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)