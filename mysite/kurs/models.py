from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    ROLES_CHOICES = (
        ('клиент', 'Клиент'),
        ('претподователь', 'Претподователь'),
    )
    user_role = models.CharField(max_length=64, choices=ROLES_CHOICES, default='клиент')
    bio = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.user_role}'


class Course(models.Model):
    course_name = models.CharField(max_length=32)
    description = models.TextField()
    LEVEL_CHOICES = (
        ('начальный', 'Начальный'),
        ('средний', 'Средний'),
        ('продвинутый', 'Продвинутый'),
    )
    course_level = models.CharField(max_length=64, choices=LEVEL_CHOICES, default='начальный')
    price = models.PositiveSmallIntegerField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_by')

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    title_name = models.CharField(max_length=64)
    video_url = models.FileField(upload_to='lesson_video/')
    content = models.TextField()
    lesson_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title_name


class Assignment(models.Model):
    assignment_title = models.CharField(max_length=64)
    description = models.TextField()
    due_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments_course')
    students = models.ManyToManyField(UserProfile, related_name='assignments')


class Exam(models.Model):
    exam_title = models.CharField(max_length=64)
    exam_course = models.FileField(upload_to='exam_course/')
    questions = models.ManyToManyField(Assignment, related_name='exams')
    passing_score = models.IntegerField()
    duration = models.DateField(auto_now_add=True)


class Certificate(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificates_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateField(auto_now_add=True)
    certificate_url = models.URLField()

    def __str__(self):
        return f"{self.student} - {self.course}"


class CourseCertificate(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f" {self.user} - {self.course} - {self.rating}"
