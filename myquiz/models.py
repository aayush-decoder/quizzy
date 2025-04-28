from django.db import models
from django.contrib.auth.models import User

from django.db import models

class QuizResult(models.Model):
    user_name = models.CharField(max_length=100)
    quiz_name = models.CharField(max_length=100)
    score = models.IntegerField()
    time_taken = models.FloatField(help_text="Time in seconds")
    rating_by_user = models.IntegerField(default=0)
    user_response = models.TextField(null=True, blank=True)
    time_response = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.quiz_name}"



class Quiz(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
    ]

    CATEGORY_CHOICES = [
        ('science', 'Science'),
        ('math', 'Math'),
        ('history', 'History'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('general knowledge', 'General Knowledge'),
    ]

    quiz_name = models.CharField(max_length=100)
    quiz_made_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes_made')
    rating = models.FloatField(default=0.0)
    quiz_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    quiz_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy')
    quiz_time = models.PositiveIntegerField(help_text="Time to complete the quiz in seconds")
    quiz_description = models.CharField(max_length=250)
    quiz_image = models.ImageField(upload_to='quiz_images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quiz_name
