from django.test import TestCase, Client

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1. Post가 하나 있다.
        post_001 = Post.objects.create(title = '첫 번째 포스트입니다.', content = 'Hello World. We are the world',)

        # 1.2. 그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(post_001.get_absoulte_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 post url로 접근하면 정상적으로 작동한다 (status code : 200).
        response = self.client.get(post_001.get_absoulte_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        navbar = soup.nav
        self.assertIn('Board', navbar.text)
        self.assertIn('Main', navbar.text)

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