# Generated by Django 4.0.2 on 2022-02-24 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_doc_dep_alter_userdetail_dep'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='dep',
        ),
    ]
