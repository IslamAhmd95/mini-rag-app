from typing import Any

from src.models import DBCollectionsEnum
from src.models.base_data_model import BaseDataModel
from src.models.db_schemas import ProjectSchema


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: Any):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DBCollectionsEnum.PROJECTS]

    async def create_project(self, project: ProjectSchema):
        result = await self.collection.insert_one(
            project.model_dump(by_alias=True, exclude_none=True)
        )
        project.id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        existing_project = await self.collection.find_one({"project_id": project_id})
        if existing_project:
            return ProjectSchema(**existing_project)

        project = ProjectSchema(project_id=project_id)
        created_project = await self.create_project(project)
        return created_project

    async def get_all_projects(self, page: int = 1, limit: int = 10):
        total_docs = await self.collection.count_documents({})
        total_pages = (total_docs // limit) + (total_docs % limit > 0)
        projects = []
        async for project in (
            self.collection.find().skip((page - 1) * limit).limit(limit)
        ):
            projects.append(ProjectSchema(**project))
        return projects, total_pages
