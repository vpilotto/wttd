# Generated by Django 2.2.5 on 2020-01-27 23:24

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('core', '0004_auto_20200123_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start', models.TimeField()),
                ('description', models.TextField()),
                ('speakers', models.ManyToManyField(to='core.Speaker')),
            ],
        ),
    ]
