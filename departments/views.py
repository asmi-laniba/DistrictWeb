from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/list.html', {'departments': departments})

def department_detail(request, dept_name):
    department = get_object_or_404(Department, name=dept_name)

    projects = department.projects.all()
    return render(request, 'departments/detail.html', {'department': department, 'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'departments/project_detail.html', {'project': project})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('department_detail', dept_name=project.department.name)
    else:
        form = ProjectForm()
    return render(request, 'departments/add_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'departments/add_project.html', {'form': form, 'edit_mode': True})
