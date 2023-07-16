from django.urls import path
from .views import *
# Ссылки этого приложения


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<int:pk>/', ShowByCategory.as_view(), name='category_list'),
    path('post/<int:pk>/', ArticleDetail.as_view(), name='post_detail'),
    path('add_article/', AddPost.as_view(), name='add'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('post/<int:pk>/update/', ArticleUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', ArticleDelete.as_view(), name='post_delete'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('search/', Search.as_view(), name='search_results'),
    path('add_comment/<int:article_id>/', add_comment, name='add_comment')
]
