"""Text extractor class for extracting text from various file formats."""

import os
from pathlib import Path
from groq import BaseModel
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from insurance_multi_agent.text_extractor.utils.helper_tools import clean_extracted_text
from insurance_multi_agent.models.entities import Document

class TextExtractor:
    """Class for extracting text from various file formats.
        1. extract text from file
        2. clean text
        3. save text
    """
    

    def extract_text_from_pdf(self, file_path)-> Document:
        """Extract text from a PDF file.

        Args:
            file_path (str): Path to the PDF file.
        Returns:
            str: Extracted text from the PDF.
        """
        print(f"Converting PDF to images...")
        images = convert_from_path(file_path)
        
        
        text = ""
        for i, image in enumerate(images):
            print(f"Processing page {i+1}...")
            page_text = pytesseract.image_to_string(image)
            text += page_text
        

        document_dict = {
            "source": file_path,
            "content": text,
            "clean_content": clean_extracted_text(text),
            "pages": len(images),
            "characters": len(text),
            "language": None
        }
    
        # Update document model with extracted text and metadata
        document = Document(**document_dict)
        return document
    


