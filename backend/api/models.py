from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    filial = models.CharField(max_length=100, null=True, blank=True)
    filial_fish = models.CharField(max_length=100, null=True, blank=True)
    filial_fish_inisiali = models.CharField(max_length=100, null=True, blank=True)
    tashkilot_nomi = models.CharField(max_length=100, null=True, blank=True)
    tashkilot_direktor_fish = models.CharField(max_length=100, null=True, blank=True)
    tashkilot_direktor_fish_inisiali = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}"

    @property
    def fish(self):
        return self.filial_fish

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class LoanApplication(models.Model):
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('moderation', 'Moderatsiyada'),
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
    )

    data = models.JSONField(verbose_name="Anketa ma'lumotlari")
    
    # Holat va Audit
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_loans')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_loans')
    
    # Snapshot ma'lumotlar (Yaratilgan vaqtdagi filial va ism)
    branch = models.CharField(max_length=100, null=True, blank=True)
    operator_fish = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ariza #{self.id} - {self.branch} ({self.status})"
