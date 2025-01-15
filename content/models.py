from django.db import models
from django.contrib.auth.models import User 


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    total_votes = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

class Rating(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} rated {self.post.title} as {self.score}"
