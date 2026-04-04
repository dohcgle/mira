from django.contrib import admin
from .models import UserProfile, LoanApplication

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fish', 'filial')
    search_fields = ('user__username', 'fish', 'filial')

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'operator_fish', 'status', 'created_at')
    list_filter = ('status', 'branch')
    search_fields = ('operator_fish', 'branch')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
