import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentHandler:
    """
    Handles PDF saving and reading operations.
    Automatically logs all actions and supports session based organizations.    
    """
    def __init__(self, data_dir=None, session_id=None):
        try:
            self.log=CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                'DATA_STORAGE_PATH',
                os.path.join(os.getcwd(), 'data', 'document_analysis'))
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
            # Create base session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            
            self.log.info("PDF Handler initilized", session_id=self.session_id, session_path=self.session_path)
        except Exception as e:
            self.log.error(f"Error Initilizing the DocumentHandler:{e}")
            raise DocumentPortalException(f"failed to Initilized the DocumentHandler",e) from e
    
    
    def save_pdf(self, uploaded_file):
        try:
            filename=os.path.basename(uploaded_file.name)
            if not filename.lower().endswith('.pdf'):
                raise DocumentPortalException(f"Invalid file uploaded. only PDF's are allowed")

            save_path=os.path.join(self.session_path, filename)
            
            with open(save_path,'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            self.log.info(f"PDF file saved successfully", filename= filename, session_id = self.session_id, save_path= save_path)
            return save_path
            
        except Exception as e:    
            self.log.error(f"Error saving the PDF:{e}")
            raise DocumentPortalException(f"failed to save the PDF",e) from e
        
    
    def read_pdf(self, pdf_path):
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text_chunks.append(f"\n--- page {page_num} ---\n{page.get_text()}")
            text = '\n'.join(text_chunks)
            self.log.info('PDF read successfully', pdf_path=pdf_path, session_id=self.session_id, pages=len(text_chunks))
            return text
        
        except Exception as e:
            self.log.error(f"Error reading the PDF:{e}")
            raise DocumentPortalException(f"failed to read the PDF",e) from e
    
    
if __name__ == '__main__':
    
    from pathlib import Path
    from io import BytesIO
    
    path = r'D:\\Datascience\\LLMOops Course\\document_portal\\data\\document_analysis\\Attention_Is_All_You_Need.pdf'

    class dummyfile:
        def __init__(self,file_path):
            self.name = Path(file_path).name 
            self._file_path= file_path
        
        def getbuffer(self):
            return open(self._file_path,'rb').read()
    
    dummy_pdf = dummyfile(path) 
    a = DocumentHandler(session_id='test_session3')
    try:        
        saved_path = a.save_pdf(dummy_pdf)
        content_pdf = a.read_pdf(saved_path)
        print(saved_path)
        print(content_pdf[:500])
    except Exception as e:
        print(f'Error:{e}')
    
        