# Generated by Django 4.2.11 on 2024-03-05 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=25)),
                ('createpassword', models.CharField(max_length=25)),
                ('Phonenumber', models.BigIntegerField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=25)),
                ('place', models.CharField(max_length=25)),
            ],
        ),
    ]
