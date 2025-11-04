from django.db import models
from django.utils.timezone import now

class ChatLog(models.Model):
    """
    Stores chatbot conversation history.
    """
    user_query = models.TextField(verbose_name="User Message")
    bot_response = models.TextField(verbose_name="Bot Response")
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Timestamp",
        db_index=True
    )

    class Meta:
        verbose_name = "Chat Log"
        verbose_name_plural = "Chat Logs"
        ordering = ['-timestamp']  # Sort by newest first

    def __str__(self):
        return f"Chat at {self.timestamp.strftime('%Y-%m-%d %H:%M')}: {self.user_query[:50]}"


class Library(models.Model):
    """
    Tracks books in the college library.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Book Title",
        db_index=True
    )
    author = models.CharField(
        max_length=100,
        verbose_name="Author"
    )
    publication_date = models.DateField(
        verbose_name="Publication Date",
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True
    )
    available_copies = models.PositiveIntegerField(
        verbose_name="Available Copies",
        default=1
    )
    image = models.ImageField(
        upload_to='book_covers/',
        verbose_name="Cover Image",
        blank=True,
        null=True
    )
    isbn = models.CharField(
        max_length=13,
        verbose_name="ISBN",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Library Book"
        verbose_name_plural = "Library Books"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"


class ChatMessage(models.Model):
    """
    Stores individual chat messages.
    """
    user_message = models.TextField(verbose_name="User Input")
    bot_response = models.TextField(verbose_name="Bot Reply")
    timestamp = models.DateTimeField(
        default=now,
        verbose_name="Created At",
        db_index=True
    )
    is_archived = models.BooleanField(
        default=False,
        verbose_name="Archived"
    )

    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d')}: {self.user_message[:30]}..."
