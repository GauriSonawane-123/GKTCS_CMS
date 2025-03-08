from django.contrib import admin
from .models import (
    User,  Content, ContentApproval, SEOData, MediaFile, 
    ContentTranslation, ContentAnalytics, Integration, SecurityLog, 
    PerformanceMetrics
)


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'phone_number')
    search_fields = ('username', 'role', 'phone_number')



@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('status', 'created_at')

@admin.register(ContentApproval)
class ContentApprovalAdmin(admin.ModelAdmin):
    list_display = ('content', 'reviewer', 'status', 'reviewed_at')
    list_filter = ('status', 'reviewed_at')

@admin.register(SEOData)
class SEODataAdmin(admin.ModelAdmin):
    list_display = ('content', 'meta_title', 'canonical_url')
    search_fields = ('meta_title', 'content__title')

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('content', 'file', 'uploaded_at')
    search_fields = ('content__title',)

@admin.register(ContentTranslation)
class ContentTranslationAdmin(admin.ModelAdmin):
    list_display = ('content', 'language', 'translated_title')
    search_fields = ('translated_title', 'content__title')

@admin.register(ContentAnalytics)
class ContentAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('content', 'views', 'likes', 'shares', 'last_accessed')
    list_filter = ('last_accessed',)

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    search_fields = ('user__username', 'action')
    list_filter = ('timestamp',)

@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ('content', 'load_time', 'cache_status', 'optimized')
    list_filter = ('cache_status', 'optimized')
