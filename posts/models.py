from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    answer_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    blocked = models.BooleanField(default=False)
    auto_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.content[:20]}...'

    def clean(self):
        if self.post.blocked:
            raise ValueError('Cannot comment on a blocked post')
        if self.answer_to and self.answer_to.blocked:
            raise ValueError('Cannot answer to a blocked comment')
        if self.answer_to and self.answer_to.post != self.post:
            raise ValueError('Answered comment must be from the same post')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
