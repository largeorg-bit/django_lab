from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from blog.forms import ArticleForm
from blog.models import Article


class ArticleListView(ListView):
    """Список только опубликованных статей."""

    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    """Страница статьи с увеличением счётчика просмотров."""

    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        article.views_count += 1
        article.save(update_fields=["views_count"])
        return article


class ArticleUpdateView(UpdateView):
    """Редактирование статьи и переход на её просмотр."""

    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"

    def get_success_url(self):
        self.success_url = reverse(
            "article_detail",
            kwargs={"pk": self.object.pk},
        )
        return self.success_url
