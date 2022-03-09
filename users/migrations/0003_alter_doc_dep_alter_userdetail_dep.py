# Generated by Django 4.0.2 on 2022-02-23 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_dep_doc_dep_userdetail_dep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='dep',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ddocs', to='users.dep'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='dep',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dusers', to='users.dep'),
        ),
    ]
