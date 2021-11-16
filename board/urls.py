from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:q>/', views.PostSearch.as_view()), # board/search/검색어 로 접근하면 PostSearch 에서 처리
    path('delete_comment/<int:pk>/', views.delete_comment), # 댓글 삭제를 위한 URL 추가
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), # 댓글 수정 페이지의 경로 추가
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()), # board/create_post 로 url 입력 시 PostCreate 클래스 사용
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),

]