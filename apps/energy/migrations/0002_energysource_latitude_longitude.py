from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='energysource',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='energysource',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
