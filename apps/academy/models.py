from django.db import models


class QuizQuestion(models.Model):
    """A single Leo Academy quiz question."""
    question_text = models.TextField()
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text[:80]


class QuestionChoice(models.Model):
    """Answer choice for a QuizQuestion."""
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} {self.choice_text}"


class LeoCandidate(models.Model):
    """Record of a completed Leo Academy quiz attempt."""
    nic = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=255)
    club_name = models.CharField(max_length=150)
    score = models.IntegerField()
    total_marks = models.IntegerField(default=20)
    is_passed = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Leo Candidate"
        verbose_name_plural = "Leo Candidates"

    def __str__(self):
        status = "PASS" if self.is_passed else "FAIL"
        return f"{self.full_name} ({self.nic}) — {status} {self.score}/{self.total_marks}"

    @property
    def percentage(self):
        if self.total_marks == 0:
            return 0
        return round((self.score / self.total_marks) * 100, 1)
