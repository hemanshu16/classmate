# Generated by Django 4.0.1 on 2022-03-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='aboutMe',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dateOfBirth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='educationDesc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='endYear',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interestDesc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='startYear',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='universityName',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
