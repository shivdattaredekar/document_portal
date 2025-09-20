import sys
import os
import fitz #type: ignore
from pathlib import Path
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    """
    
    """

    def __init__(self, base_dir: str = "data\\document_compare"):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_existing_file(self):
        """
        deletes the existing file in the base directory.
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info(f"Deleted existing file", path = str(file))
                self.log.info("All existing files deleted successfully from the directory", directory=str(self.base_dir))
        except Exception as e:
            self.log.error(f"Error occurred while deleting the file: {e}")
            raise DocumentPortalException("Failed to delete the file", sys)

    def save_uploaded_files(self, reference_file, actual_file):
        """
        saves the uploaded file to the base directory.
        """
        try:
            self.delete_existing_file()
            self.log.info('Existing file deleted successfully')
            # Save the new file logic here
            reference_path = self.base_dir / reference_file.name
            actual_path = self.base_dir / actual_file.name
            
            if not (reference_file.name.endswith('.pdf') and actual_file.name.endswith('.pdf')):
                raise ValueError("Only PDF files are supported.")
            
            with open(reference_path, 'wb') as f:
                f.write(reference_file.getbuffer())

            with open(actual_path, 'wb') as f:
                f.write(actual_file.getbuffer())

            self.log.info(f"Files saved successfully", reference_file=str(reference_path), actual_file=str(actual_path))

            return reference_path, actual_path
        
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

                self.log.info(f"Extracted text successfully", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)

        except Exception as e:
            self.log.error(f"Error occurred while reading PDF file: {e}")
            raise DocumentPortalException("Failed to read the pdf", sys) 
        
    def combine_documents(self) -> str:
        """
        Combines the text from the two PDF files.
        
        """
        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == '.pdf':
                    content_dict[filename.name] = self.read_pdf(filename)
            
            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text = f"\n\n".join(doc_parts)
            self.log.info("Documents combined successfully", count = len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.log.error(f"Error occurred while combining documents: {e}")
            raise DocumentPortalException("Failed to combine the documents", sys)
