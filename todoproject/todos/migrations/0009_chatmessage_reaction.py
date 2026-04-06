from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('todos', '0008_chatmessage')]
    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='reaction',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
