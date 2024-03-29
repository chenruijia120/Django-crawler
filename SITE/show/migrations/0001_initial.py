# Generated by Django 3.0.3 on 2020-09-09 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True, verbose_name='名字')),
                ('desc', models.CharField(max_length=500, null=True, verbose_name='人物简介')),
                ('pic_link', models.CharField(max_length=500, null=True, verbose_name='照片')),
                ('otherinfo', models.CharField(max_length=500, null=True, verbose_name='其他信息')),
                ('other', models.CharField(max_length=500, null=True, verbose_name='其他')),
            ],
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True, verbose_name='电影标题')),
                ('desc', models.CharField(max_length=500, null=True, verbose_name='电影简介')),
                ('pic_link', models.CharField(max_length=500, null=True, verbose_name='海报')),
                ('director', models.CharField(max_length=500, null=True, verbose_name='导演')),
                ('screenwriter', models.CharField(max_length=500, null=True, verbose_name='编剧')),
                ('type', models.CharField(max_length=500, null=True, verbose_name='类型')),
                ('comment1', models.CharField(max_length=500, null=True, verbose_name='短评1')),
                ('comment2', models.CharField(max_length=500, null=True, verbose_name='短评2')),
                ('comment3', models.CharField(max_length=500, null=True, verbose_name='短评3')),
                ('comment4', models.CharField(max_length=500, null=True, verbose_name='短评4')),
                ('comment5', models.CharField(max_length=500, null=True, verbose_name='短评5')),
                ('actors', models.ManyToManyField(through='show.MemberShip', to='show.Actor')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Movie'),
        ),
    ]
