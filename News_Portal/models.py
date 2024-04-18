from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache




class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def rating_update(self):
        posts_rating = 0
        comments_rating = 0
        posts_comments_rating = 0
        posts = Post.objects.filter(author=self)
        for p in posts:
            posts_rating += p.rating
        comments = Comment.objects.filter(user=self.user)
        for c in comments:
            comments_rating += c.rating
        posts_comments = Comment.objects.filter(post__author=self)
        for pc in posts_comments_rating:
            posts_comments_rating += pc.rating

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name.title()

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = 'a'
    news = 'n'
    SELECT = [(article,"статья"), (news, 'новость')]
    type = models.CharField(max_length=1, choices=SELECT, default=news)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    statement = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(verbose_name='Рейтинг статьи',default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + "..."
        else:
            return self.text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(verbose_name='Рейтинг комментария', default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
