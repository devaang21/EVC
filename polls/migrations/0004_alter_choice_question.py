# Generated by Django 4.0.6 on 2022-07-07 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_choice_question_question_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(default='?', on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
        ),
    ]
