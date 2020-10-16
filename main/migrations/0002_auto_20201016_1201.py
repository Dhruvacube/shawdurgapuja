# Generated by Django 3.1.1 on 2020-10-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='maacomevid',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Will there be any video for the Maa Durga coming to home'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='day',
            field=models.CharField(blank=True, choices=[('E', 'Ekum'), ('D', 'Dvitia'), ('T', 'Tritiya'), ('C', 'Maha Chathurti'), ('P', 'Maha Panchami'), ('S', 'Maha Shashti'), ('SA', 'Maha Saptami'), ('A', 'Maha Ashtami'), ('SAN', 'Sandhi Puja'), ('N', 'Maha Navami'), ('D', 'Maha Dashami')], default='S', max_length=50, null=True, verbose_name='Day of Uploading'),
        ),
    ]
