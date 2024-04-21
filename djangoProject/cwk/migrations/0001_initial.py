# Generated by Django 4.1 on 2024-04-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoryModel',
            fields=[
                ('uniqueKey', models.AutoField(primary_key=True, serialize=False)),
                ('headline', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=10)),
                ('region', models.CharField(max_length=2)),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('details', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]