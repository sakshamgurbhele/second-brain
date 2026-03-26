from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0007_link_codesnippet_java'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('sender', models.CharField(choices=[('me', 'Me'), ('her', 'Her')], max_length=3)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['sent_at'],
            },
        ),
    ]
