from import_export import resources
from .models import Project, SubProject


class ProjectResources(resources.ModelResource):
    class Meta:
        model = Project
