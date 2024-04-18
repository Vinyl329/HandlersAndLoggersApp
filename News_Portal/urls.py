from django.urls import path
from .views import NewsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryListView, subscribe
from .views import upgrade_me
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*5)(NewsList.as_view())),
    path('<int:pk>', cache_page(60*1)(PostDetail.as_view())),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', cache_page(60*10)(CategoryListView.as_view()), name='categories_view'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]