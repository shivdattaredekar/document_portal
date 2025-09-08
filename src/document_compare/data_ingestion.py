import sys
import os
import fitz
from pathlib import Path
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    """
    
    """

    def __init__(self, base_dir: str):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_existing_file(self):
        """
        deletes the existing file in the base directory.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred while deleting the file: {e}")
            raise DocumentPortalException("Failed to delete the file", sys)

    def save_uploaded_file(self):
        """
        saves the uploaded file to the base directory.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred while saving the file: {e}")
            raise DocumentPortalException("Failed to save the file", sys)
        
    def read_pdf(self, pdf_path: Path) -> str:
        """
        Gets the the PDF file and extract text from it.
        """
        try:
            with fitz.open(str(pdf_path)) as doc:
                if doc.is_encrypted:
                    raise ValueError("The PDF file is encrypted and cannot be read.")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text=page.get_text()
                    if text.strip():
                        all_text.append(f"\n --- Page{page_num + 1} --- \n")

                log.info(f"Extracted text successfully", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)

        except Exception as e:
            self.log.error(f"Error occurred while reading PDF file: {e}")
            raise DocumentPortalException("Failed to read the pdf", sys) 
