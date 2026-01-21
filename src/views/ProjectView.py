import os

from .BaseView import BaseView


class ProjectView(BaseView):
    def __init__(self) -> None:
        super().__init__()

    def get_project_dir_path(self, project_id):
        project_dir_path = os.path.join(
            self.files_dir_path,
            project_id
        )

        if not os.path.exists(project_dir_path):
            os.makedirs(project_dir_path)

        return project_dir_path