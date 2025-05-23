# Generated by Django 5.1.7 on 2025-04-25 20:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('d', 'Dog'), ('c', 'Cat'), ('f', 'Fish'), ('s', 'Small Mammal'), ('b', 'Bird'), ('r', 'Reptile')], default='d', max_length=1)),
                ('breed', models.CharField(max_length=30)),
                ('sex', models.CharField(choices=[('f', 'Female'), ('m', 'Male')], default='f', max_length=1)),
                ('pfp', models.ImageField(blank=True, null=True, upload_to='pet_profiles/')),
                ('dob', models.DateTimeField()),
                ('weight', models.FloatField()),
                ('spayed', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('non_owners', models.ManyToManyField(blank=True, related_name='authorized_users', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets_owner', to=settings.AUTH_USER_MODEL)),
                ('vet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pets_vet', to='users.vet')),
            ],
        ),
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('feed_type', models.CharField(choices=[('gen', 'General Update'), ('inq', 'Inquiry to Vet')], default='gen', max_length=3)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_solved', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feed_items_created_by', to=settings.AUTH_USER_MODEL)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feed_items', to='pets.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='pets.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('last_done', models.DateTimeField()),
                ('next_due', models.DateTimeField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='pets.pet')),
            ],
        ),
    ]
