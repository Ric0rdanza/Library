# Generated by Django 3.1 on 2020-09-06 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=128, unique=True)),
                ('bookname', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('publisher', models.CharField(max_length=30)),
                ('stock', models.IntegerField()),
                ('description', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=11)),
                ('is_manager', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.book')),
                ('readerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.reader')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.book')),
                ('readerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.reader')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=400)),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.book')),
                ('readerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.reader')),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.book')),
                ('readerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.reader')),
            ],
        ),
    ]
