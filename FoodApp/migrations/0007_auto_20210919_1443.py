# Generated by Django 3.0.5 on 2021-09-19 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0006_ordersummary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersummary',
            name='date',
            field=models.CharField(default=' 2021-09-19 Sep:09 ', max_length=10),
        ),
        migrations.AlterModelTable(
            name='ordersummary',
            table='OrderSummary',
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalprice', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('foodobj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FoodApp.Food')),
                ('ordersobj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FoodApp.OrderSummary')),
            ],
            options={
                'db_table': 'Orders',
            },
        ),
    ]
