# Generated by Django 3.1 on 2020-09-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20200907_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewBorrowlistWithStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=254)),
                ('bookname', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('publisher', models.CharField(max_length=30)),
                ('status', models.IntegerField()),
            ],
        ),
    ]
