from django.db import models
from enum import Enum
from datetime import timedelta
from django.db.models import Sum
from authorization.models import CustomUser
from django.utils import timezone
from django.conf import settings
import os
from django.core.files.storage import default_storage
import uuid


def shoes_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    upload_to = f'shoes_images/{instance.product.id_shoes}/{unique_filename}'
    storage = default_storage
    storage.save(upload_to, instance.image)

    return upload_to

def collections_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    upload_to = f'collections_images/{instance.collection.id_collection}/{unique_filename}'
    storage = default_storage
    storage.save(upload_to, instance.c_image)

    return upload_to

def get_shoe_images(instance):
        # Шлях до папки зображень
        image_dir = os.path.join(settings.MEDIA_ROOT, f"shoes_images/{instance.product.id_shoes}")
        if not os.path.exists(image_dir):
            return []
        # Отримуємо список файлів у папці
        return [os.path.join(settings.MEDIA_URL, f"shoes_images/{instance.product.id_shoes}/{file}") for file in os.listdir(image_dir)]

def get_collection_images(instance):
        # Шлях до папки зображень
        image_dir = os.path.join(settings.MEDIA_ROOT, f"collections_images/{instance.collection.id_collection}")
        if not os.path.exists(image_dir):
            return []
        # Отримуємо список файлів у папці
        return [os.path.join(settings.MEDIA_URL, f"collections_images/{instance.collection.id_collection}/{file}") for file in os.listdir(image_dir)]


class Order_status(Enum):
    ACCEPTED = 'accepted'
    PAID = 'paid'
    IN_PROCESSING = 'in processing'
    delivered = 'delivered'

class Shoe_gender(Enum):
    FEMALE = 'female'
    MALE = 'male'
    BOY = 'boy'
    GIRL = 'girl'

class Collection(models.Model):
    id_collection = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=100, null=False, blank=False)
    c_description = models.CharField(max_length=250)
    c_slug = models.SlugField(default='', null=False, blank=False)

    def get_pk(self):
        return self.id_collection

    def __str__(self):
        return self.c_name

class CollectionImage(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='c_images')
    c_image = models.FileField(upload_to=collections_image_upload_to)

    def get_collection_images(self):
        return [image.image.url for image in self.c_images.all()]


class Shoes(models.Model):
    id_shoes = models.AutoField(primary_key=True, unique=True)
    sh_name = models.CharField(max_length=255)
    sh_model = models.CharField(max_length=255)
    sh_size = models.IntegerField(null=False, default=38)
    sh_color = models.CharField(max_length=255)
    sh_manufacturer = models.CharField(max_length=255, blank=True, null=True)
    sh_count = models.IntegerField(null=False, default=1)
    sh_price = models.DecimalField(max_digits=10, decimal_places=2)
    sh_slug = models.SlugField(default='', null=False, blank=False)

    sh_gender = models.CharField(max_length=45, blank=True, null=False,
                                 default=Shoe_gender.FEMALE, choices=[(gender.value, gender.name) for gender in Shoe_gender])
    collection = models.ForeignKey(Collection, null=True, on_delete=models.SET_NULL, related_name='sh_collection')

    class Meta:
        db_table = 'shoes'

    def get_images(self):
        return [image.image.url for image in self.images.all()]

    def get_pk(self):
        return self.id_shoes

    def __str__(self):
        return self.sh_name

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE)


class ProductImage(models.Model):
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=shoes_image_upload_to)

class Orders(models.Model):
    id_order = models.AutoField(primary_key=True, verbose_name='#')
    o_shoes = models.ForeignKey(
        Shoes, on_delete=models.DO_NOTHING, db_column='o_shoes', verbose_name="Shoes"
    )
    o_count = models.IntegerField(null=False, default=1, verbose_name="Count")
    o_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    o_recipient_first_name = models.CharField(max_length=45, null=False, default='Name', verbose_name="Recipient name")
    o_recipient_last_name = models.CharField(max_length=45, null=False, default='Surname', verbose_name="Recipient surname")
    o_address = models.CharField(max_length=100, null=False, default='Address', verbose_name="Address")
    o_email = models.CharField(max_length=100, null=False, default='Email', verbose_name="Email")
    o_phone_number = models.CharField(max_length=13, null=False, default='Phone Number', verbose_name="Phone Number")
    o_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Comment")
    o_status = models.CharField(
        max_length=45, default=Order_status.ACCEPTED.value,
        choices=[(status.value, status.name) for status in Order_status],
        verbose_name="Order Status"
    )
    o_user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, null=True, db_column='o_user', verbose_name="User"
    )
    o_date_created = models.DateTimeField(default=timezone.now, verbose_name="Date Created")

    def get_pk(self):
        return self.id_order

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'

    @classmethod
    def calculate_analytics(cls):
        current_year = timezone.now().year
        current_month = timezone.now().month
        first_day_of_current_month = timezone.now().replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

        analytics = cls.objects.aggregate(
            total_sum=models.Sum('o_sum'),
            average_sum=models.Avg('o_sum'),
            max_sum=models.Max('o_sum'),
            min_sum=models.Min('o_sum'),
            total_sum_current_month=models.Sum(
                'o_sum',
                filter=models.Q(o_date_created__year=current_year, o_date_created__month=current_month)
            ),
            total_sum_previous_month=models.Sum(
                'o_sum',
                filter=models.Q(o_date_created__year=last_day_of_previous_month.year,
                                o_date_created__month=last_day_of_previous_month.month)
            )
        )
        return analytics