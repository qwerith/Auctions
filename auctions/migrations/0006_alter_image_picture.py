# Generated by Django 3.2.7 on 2021-10-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_image_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='picture',
            field=models.ImageField(default='commerce_1_Diagram.drawio.png', upload_to='media/'),
        ),
    ]