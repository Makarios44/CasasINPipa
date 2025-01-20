# Generated by Django 5.1.4 on 2025-01-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_casa_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='casa',
            name='capacidade_maxima',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='casa',
            name='disponivel_ate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='casa',
            name='disponivel_de',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='casa',
            name='imagem_principal',
            field=models.ImageField(blank=True, null=True, upload_to='casas/'),
        ),
    ]
