from django.db import models
import uuid
# Create your models here.


class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255, blank=True)
    app_secret_token = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.account_id:
            self.account_id = self.generate_account_id()
        if not self.app_secret_token:
            self.app_secret_token = self.generate_app_secret_token()
        super().save(*args, **kwargs)

    def generate_account_id(self):
        return f'{uuid.uuid4().hex}APPID{uuid.uuid4().hex}'

    def generate_app_secret_token(self):
        return uuid.uuid4().hex

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=20)
    headers = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.account.account_name} {str(self.id)}"