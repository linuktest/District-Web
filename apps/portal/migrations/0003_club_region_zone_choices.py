from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_event_president_attending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='meeting_details',
        ),
        migrations.AlterField(
            model_name='club',
            name='region',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B')], max_length=2),
        ),
        migrations.AlterField(
            model_name='club',
            name='zone',
            field=models.CharField(choices=[('A', 'A'), ('A1', 'A1'), ('B', 'B'), ('B1', 'B1')], max_length=2),
        ),
    ]
