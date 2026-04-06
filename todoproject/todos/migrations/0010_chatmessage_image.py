from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('todos', '0009_chatmessage_reaction')]
    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images/'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='content',
            field=models.TextField(max_length=2000, blank=True, default=''),
        ),
    ]
