from django.db import models

class QuizResult(models.Model):
    user_name = models.CharField(max_length=100)
    quiz_name = models.CharField(max_length=100)
    score = models.IntegerField()
    time_taken = models.FloatField(help_text="Time in seconds")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.quiz_name} ({self.score}) in {self.time_taken}s"
