from django.db import migrations


def forwards(apps, schema_editor):
    Task = apps.get_model('board', 'Task')
    Space = apps.get_model('board', 'Space')
    for task in Task.objects.all():
        ws_name = (task.workspace or 'office').strip()
        if not ws_name:
            ws_name = 'office'
        space, created = Space.objects.get_or_create(name=ws_name)
        task.workspace_fk = space
        task.save()


def backwards(apps, schema_editor):
    Task = apps.get_model('board', 'Task')
    for task in Task.objects.all():
        if task.workspace_fk:
            task.workspace = task.workspace_fk.name
            task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_task_workspace_fk'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
