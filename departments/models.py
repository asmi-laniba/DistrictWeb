from django.db import models

class Department(models.Model):
    NAME_CHOICES = (
        ('health', 'Health'),
        ('education', 'Education'),
        ('revenue', 'Revenue'),
        ('public_works', 'Public Works'),
        ('police', 'Police'),
    )
    name = models.CharField(max_length=50, choices=NAME_CHOICES, unique=True)
    head = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()

class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    )
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    budget_used = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    progress = models.IntegerField(default=0) # 0 to 100
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class DepartmentMetric(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='metrics')
    label = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.department.name} - {self.label}: {self.value} {self.unit}"
