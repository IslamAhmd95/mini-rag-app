import os

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .BaseView import BaseView
from .ProjectView import ProjectView
from src.models import ExtensionEnum


class ProcessView(BaseView):
    def __init__(self, project_id) -> None:
        super().__init__(project_id)
        self.project_path = ProjectView(project_id=self.project_id).get_project_dir_path()

    def get_file_extention(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_path = os.path.join(
            self.project_path,
            file_id
        )
        file_ext = self.get_file_extention(file_id=file_id)

        if file_ext == ExtensionEnum.TXT:
            return TextLoader(file_path, encoding='utf-8')

        if file_ext == ExtensionEnum.PDF:
            return PyMuPDFLoader(file_path)
            
        return None     

    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()

        return None

    def process_file_content(self, file_content: list, chunk_size: int=100, overlap_size: int=20):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size)

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks

