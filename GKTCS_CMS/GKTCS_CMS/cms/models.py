from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
# 1. User Roles & Authentication
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('contributor', 'Contributor'),
        ('viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')

    def _str_(self):
        return f"{self.username} ({self.role})"
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="cmsuser", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="cmsuser_permissions", blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        
    class CMSUser(models.Model):  
        username = models.CharField(max_length=150, unique=True)
        role = models.CharField(max_length=50)
        phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'cmsuser' 
# 2. Content Model
class Content(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return self.title

# 3. Content Approval & Workflow
class ContentApproval(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approvals")
    status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.content.title} - {self.status}"

# 4. SEO & Metadata
class SEOData(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    keywords = models.CharField(max_length=255)
    canonical_url = models.URLField(blank=True, null=True)

    def _str_(self):
        return self.meta_title

# 5. Media & File Management
class MediaFile(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.file.name

# 6. Multi-Language Support
class ContentTranslation(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)  # e.g., 'en', 'fr', 'es'
    translated_title = models.CharField(max_length=255)
    translated_body = models.TextField()

    def _str_(self):
        return f"{self.content.title} - {self.language}"

# 7. Analytics & Reporting
class ContentAnalytics(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.content.title} - {self.views} Views"

# 8. Third-Party Integrations
class Integration(models.Model):
    SERVICE_CHOICES = [
        ('google_analytics', 'Google Analytics'),
        ('crm', 'CRM System'),
        ('social_media', 'Social Media API'),
    ]

    name = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.name

# 9. Security & Compliance
class SecurityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def _str_(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"

# 10. Performance Optimization
class PerformanceMetrics(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    load_time = models.FloatField()  # in seconds
    cache_status = models.CharField(max_length=50, choices=[('hit', 'Cache Hit'), ('miss', 'Cache Miss')])
    optimized = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.content.title} - {self.load_time}s Load Time"
