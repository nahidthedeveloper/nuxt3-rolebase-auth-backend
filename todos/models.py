from django.db import models
from authentication.models import Account

class Todos(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    todo = models.TextField(blank=False, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return f'{self.todo}'
