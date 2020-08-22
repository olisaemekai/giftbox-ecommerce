from django.db import models
from django.urls import reverse

# for taggit
# from taggit.managers import TaggableManager 


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(upload_to='tags/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_tag', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

class BoxItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def total_price(self):
        return self.quantity * self.product.price

class Box(models.Model):
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='custom_box_images/%Y/%m/%d', blank=True)
    items = models.ManyToManyField(BoxItem)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'box'
        verbose_name_plural = 'boxes'
    
    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

    def get_absolute_url(self):
        return reverse('shop:box_detail', args=[self.id])

