from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Space
from django.views.decorators.http import require_POST

def board_view(request):
	# Load available spaces from DB
	spaces = list(Space.objects.values_list('name', flat=True))
	default_space = spaces[0] if spaces else 'office'

	# Get current workspace from session, default to first space or 'office'
	current_workspace = request.session.get('current_workspace', default_space)
	
	# Handle workspace switching via GET param
	if 'workspace' in request.GET:
		new_workspace = request.GET.get('workspace')
		if new_workspace in spaces:
			current_workspace = new_workspace
			request.session['current_workspace'] = current_workspace
			return redirect('board')

	# If current workspace got deleted or doesn't exist, fallback
	if current_workspace not in spaces:
		current_workspace = default_space
		request.session['current_workspace'] = current_workspace

	statuses = [
		("planned", "Planned"),
		("in-progress", "In Progress"),
		("in-review", "In Review"),
		("done", "Done"),
		("cancelled", "Cancelled"),
	]

	# Filter tasks by current workspace (workspace is a FK to Space)
	tasks_by_status = {key: Task.objects.filter(status=key, workspace__name=current_workspace) for key, _ in statuses}

	return render(request, "board/board.html", {
		"statuses": statuses, 
		"tasks_by_status": tasks_by_status,
		"current_workspace": current_workspace,
		"spaces": spaces,
	})

def create_task(request):
	# Get current workspace from session, default to first space or 'office'
	spaces = list(Space.objects.values_list('name', flat=True))
	default_space = spaces[0] if spaces else 'office'
	current_workspace = request.session.get('current_workspace', default_space)
	
	if request.method == "POST":
		short_description = request.POST.get("short_description")
		description = request.POST.get("description")
		priority = request.POST.get("priority", "normal")
		if short_description and description:
			# Ensure we have a Space instance for the current workspace
			space_obj, _ = Space.objects.get_or_create(name=current_workspace)
			is_working = request.POST.get('is_working') == 'on'
			Task.objects.create(
				short_description=short_description, 
				description=description, 
				status="planned",
				workspace=space_obj,
				priority=priority,
				is_working=is_working
			)
			return redirect("board")
	return render(request, "board/create.html", {"current_workspace": current_workspace})

@require_POST
def update_task_status(request, task_id):
	task = get_object_or_404(Task, id=task_id)
	new_status = request.POST.get("status")
	if new_status in dict(Task.STATUS_CHOICES):
		task.status = new_status
		task.save()
	return redirect("board")

def task_detail(request, task_id):
	task = get_object_or_404(Task, id=task_id)
	if request.method == "POST":
		# Main save button saves entire task
		if 'save' in request.POST:
			task.short_description = request.POST.get("short_description", task.short_description)
			task.description = request.POST.get("description", task.description)
			# save priority if provided
			if 'priority' in request.POST:
				task.priority = request.POST.get('priority', task.priority)
			# save is_working checkbox state (checkbox absent when unchecked)
			task.is_working = 'is_working' in request.POST
			# comments may be present in the main form as well
			if 'comments' in request.POST:
				task.comments = request.POST.get("comments", task.comments)
			task.save()
		# Separate comments-only form
		elif 'comments' in request.POST:
			task.comments = request.POST.get("comments", task.comments)
			task.save()
		# Allow toggling is_working from a form that only submits that flag
		elif 'is_working' in request.POST:
			task.is_working = 'is_working' in request.POST
			task.save()
		# Also allow priority-only post (if the form only sent priority)
		elif 'priority' in request.POST:
			task.priority = request.POST.get('priority', task.priority)
			task.save()
		return redirect('task_detail', task_id=task.id)
	return render(request, "board/task_detail.html", {"task": task})

@require_POST
def delete_task(request, task_id):
	task = get_object_or_404(Task, id=task_id)
	task.delete()
	return redirect("board")
