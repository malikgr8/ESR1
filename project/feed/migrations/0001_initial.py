# Generated by Django 3.1.7 on 2021-03-10 15:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import project.feed.models.user_profile


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='category_name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_till', models.DateTimeField()),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('discounted_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('original_price', models.FloatField(default=0.0)),
                ('image_url', models.ImageField(upload_to='')),
                ('valid_from', models.DateTimeField()),
                ('valid_till', models.DateTimeField()),
                ('approval_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='restaurant_name')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('street', models.CharField(max_length=50, verbose_name='restaurant_street')),
                ('city', models.CharField(max_length=50, verbose_name='restaurant_city')),
                ('zip', models.CharField(blank=True, max_length=10, verbose_name='restaurant_zip')),
                ('website', models.URLField(blank=True, verbose_name='restaurant_website')),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='restaurant_phone_number')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='restaurant_email')),
                ('opening_hours', models.CharField(max_length=50, verbose_name='restaurant_opening_hours')),
                ('price_level', models.CharField(choices=[('LOW', '$'), ('MEDIUM', '$$'), ('HIGH', '$$$')], max_length=6, verbose_name='restaurant_price_level')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date_modified')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='restaurant_image')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='restaurants', to='feed.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='restaurants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='review_comment')),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='restaurant_rating')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.offer')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.restaurant')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-created_at'],
                'unique_together': {('user_id', 'restaurant_id')},
            },
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_at', models.DateTimeField(auto_now_add=True)),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feed.coupon')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30, verbose_name='user_location')),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='user_phone_number')),
                ('things_love', models.TextField(verbose_name='things_user_love')),
                ('description', models.TextField(verbose_name='user_description')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('registration_code', models.CharField(default=project.feed.models.user_profile.code_generator, max_length=15, verbose_name='registration_code')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feed.restaurant'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='feed.offer'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='review_comment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date_modified')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='feed.review')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-modified'],
            },
        ),
        migrations.CreateModel(
            name='ReviewLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='feed.review')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review like',
                'verbose_name_plural': 'Review likes',
                'unique_together': {('user', 'review')},
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='feed.comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CommentLike',
                'verbose_name_plural': 'Comment likes',
                'unique_together': {('user', 'comment')},
            },
        ),
    ]
