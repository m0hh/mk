# Generated by Django 4.0.2 on 2022-03-01 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_userdetail_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='rank',
            field=models.CharField(choices=[('saf', 'SAF'), ('zabet', 'ZABET'), ('superzabet', 'SUPERZABET'), ('modeer', 'MODEER'), ('raeesarkan', 'RAEESARKAN')], default='saf', max_length=100),
        ),
    ]