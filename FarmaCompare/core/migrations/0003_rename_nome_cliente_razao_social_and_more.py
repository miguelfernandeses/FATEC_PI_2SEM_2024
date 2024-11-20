# Generated by Django 5.1.1 on 2024-11-18 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_produto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='nome',
            new_name='razao_social',
        ),
        migrations.RemoveField(
            model_name='cadastromodel',
            name='nome',
        ),
        migrations.AddField(
            model_name='cadastromodel',
            name='cnpj',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cadastromodel',
            name='endereco',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cadastromodel',
            name='razao_social',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='cadastromodel',
            name='telefone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plano', models.IntegerField(choices=[(1, 'Grátis'), (2, 'Mensal'), (3, 'Anual')], default=1)),
                ('data_assinatura', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]