# Generated by Django 4.2.1 on 2023-06-04 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittlelemonAPI', '0002_category_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='Category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LittlelemonAPI.category'),
        ),
    ]