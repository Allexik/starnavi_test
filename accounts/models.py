from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auto_response = models.BooleanField(default=False)
    auto_response_delay = models.IntegerField(default=0)  # in seconds  (can be normalized)

    def __str__(self):
        return self.user.username
