# Generated by Django 4.1.3 on 2023-01-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AlterField(
            model_name='gene',
            name='end_position',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='gene',
            name='start_position',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='proteine',
            name='end_position',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='proteine',
            name='start_position',
            field=models.IntegerField(),
        ),
    ]
