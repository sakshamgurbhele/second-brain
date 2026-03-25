import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0006_codesnippet'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2000)),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('tags', models.CharField(blank=True, default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='codesnippet',
            name='language',
            field=models.CharField(
                choices=[
                    ('python', 'Python'), ('javascript', 'JavaScript'),
                    ('typescript', 'TypeScript'), ('htmlmixed', 'HTML'),
                    ('css', 'CSS'), ('shell', 'Shell'), ('java', 'Java'),
                    ('go', 'Go'), ('rust', 'Rust'), ('sql', 'SQL'),
                    ('yaml', 'YAML'), ('xml', 'XML'), ('markdown', 'Markdown'),
                    ('text', 'Plain Text'),
                ],
                default='python', max_length=20,
            ),
        ),
    ]
