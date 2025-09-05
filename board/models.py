from django.db import models

class Task(models.Model):
	STATUS_CHOICES = [
		("planned", "Planned"),
		("in-progress", "In Progress"),
		("in-review", "In Review"),
		("done", "Done"),
		("cancelled", "Cancelled"),
	]
	PRIORITY_CHOICES = [
		('low', 'Low'),
		('normal', 'Normal'),
		('high', 'High'),
	]
	
	short_description = models.CharField(max_length=100)
	description = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
	workspace = models.ForeignKey('Space', null=True, blank=True, on_delete=models.CASCADE, related_name='tasks')
	comments = models.TextField(blank=True, default="")
	priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
	is_working = models.BooleanField(default=False) # Indicates someone is currently working on the task

	def __str__(self):
		return self.short_description

class Space(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
