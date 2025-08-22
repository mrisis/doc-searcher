from django.db import models
from django.contrib.auth.models import User



class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    file = models.FileField(upload_to='documents/', verbose_name="فایل")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "سند"
        verbose_name_plural = "اسناد"