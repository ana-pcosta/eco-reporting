from llama_index.core import SimpleDirectoryReader
from ecoreporter import ROOT_PATH
import re
from typing import List, Union


class ReferenceHandler:
    def __init__(self, data_path: str):
        """
        Handler class to setup the references used downstream for content generation and evaluation.
        """
        self.data_path = data_path

        self.documents = SimpleDirectoryReader(data_path).load_data()

    def get_reference_text(self, filename: str, pages: Union[List, str] = "all"):
        filename_docs = [
            doc for doc in self.documents if doc.metadata["file_name"] == filename
        ]
        sorted_filename_docs = sorted(
            filename_docs, key=lambda x: x.metadata.get("page_label", 0)
        )

        if pages != "all":
            sorted_filename_docs = [
                page
                for page in sorted_filename_docs
                if int(page.metadata.get("page_label")) in pages
            ]

        return self.clean_text(
            ("\n\n").join([doc.text for doc in sorted_filename_docs])
        )

    def clean_text(self, text: str) -> str:
        # Remove excess whitespace, tabs, newlines
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text
