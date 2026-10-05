from django.urls import path

from blog.views import ArticleDetailView, ArticleListView, ArticleUpdateView

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path(
        "articles/<int:pk>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "articles/<int:pk>/edit/",
        ArticleUpdateView.as_view(),
        name="article_update",
    ),
]
