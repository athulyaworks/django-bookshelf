from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100) 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review for {self.book.title} by {self.reviewer.username}"

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favourited_by')

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class UserBookStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_statuses')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_statuses')
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} read: {self.is_read}"

