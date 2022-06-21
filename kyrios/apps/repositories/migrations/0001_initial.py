# Generated by Django 4.0.5 on 2022-06-21 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RepositoryAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RepositoryStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RepositoryTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postOnProfile', models.BooleanField(default=False)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repositories.repository')),
            ],
        ),
    ]
