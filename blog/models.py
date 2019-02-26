from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager
from martor.models import MartorField

from django.utils.text import slugify

#from
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    #body = models.TextField()
    body = MartorField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    
    objects = models.Manager()# The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager() # Our tags manager.
    
    def save(self, *args, **kwargs):
        #if not self.slug:
        print('XXXXXX')
        self.slug = vi_slug(self.slug)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        #tmp_slug = slugify(self.slug)
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

# Class comment
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    #body = MartorField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

def vi_slug(data):
    vietnamese_map = {
        ord(u'o'): 'o', ord(u'ò'): 'o', ord(u'ó'): 'o', ord(u'ỏ'): 'o', ord(u'õ'): 'o', ord(u'ọ'): 'o',
        ord(u'ơ'): 'o', ord(u'ờ'): 'o', ord(u'ớ'): 'o', ord(u'ở'): 'o', ord(u'ỡ'): 'o', ord(u'ợ'): 'o',
        ord(u'ô'): 'o', ord(u'ồ'): 'o', ord(u'ố'): 'o', ord(u'ổ'): 'o', ord(u'ỗ'): 'o', ord(u'ộ'): 'o',

        ord(u'à'): 'a', ord(u'á'): 'a', ord(u'á'): 'a', ord(u'ả'): 'a', ord(u'ã'): 'a', ord(u'ạ'): 'a',
        ord(u'ă'): 'a', ord(u'ắ'): 'a', ord(u'ằ'): 'a', ord(u'ẳ'): 'a', ord(u'ẵ'): 'a', ord(u'ạ'): 'a',
        ord(u'â'): 'a', ord(u'ầ'): 'a', ord(u'ấ'): 'a', ord(u'ậ'): 'a', ord(u'ẫ'): 'a', ord(u'ẩ'): 'a',

        ord(u'đ'): 'd', ord(u'Đ'): 'd',

        ord(u'è'): 'e', ord(u'é'): 'e', ord(u'ẻ'): 'e', ord(u'ẽ'): 'e', ord(u'ẹ'): 'e',
        ord(u'ê'): 'e', ord(u'ề'): 'e', ord(u'ế'): 'e', ord(u'ể'): 'e', ord(u'ễ'): 'e', ord(u'ệ'): 'e',

        ord(u'ì'): 'i', ord(u'í'): 'i', ord(u'ỉ'): 'i', ord(u'ĩ'): 'i', ord(u'ị'): 'i',
        ord(u'ư'): 'u', ord(u'ừ'): 'u', ord(u'ứ'): 'u', ord(u'ử'): 'ữ', ord(u'ữ'): 'u', ord(u'ự'): 'u',
        ord(u'ý'): 'y', ord(u'ỳ'): 'y', ord(u'ỷ'): 'y', ord(u'ỹ'): 'y', ord(u'ỵ'): 'y',
    }
    slug = slugify(str(data).translate(vietnamese_map))
    return slug
