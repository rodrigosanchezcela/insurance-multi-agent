"""file for helper functions regarding text extraction from insurance documents."""
import re

def clean_extracted_text(text: str) -> str:

    """
    Clean OCR-extracted text from insurance documents.
    
    Args:
        text: Raw OCR text with noise and formatting issues
        
    Returns:
        Cleaned text with reduced noise and no empty lines
    """
    # Remove excessive whitespace and newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove standalone special characters and noise
    text = re.sub(r'\s+[|!]{2,}\s+', ' ', text)
    text = re.sub(r'\s+[VW]{2,}\s+', ' ', text)
    
    # Clean up excessive dashes and separators
    text = re.sub(r'[-=]{5,}', '', text)
    
    # Remove isolated single/double characters that are likely noise
    text = re.sub(r'\s+[A-Z]{1,2}\s+(?=[A-Z])', ' ', text)
    
    # Clean up multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove lines with mostly special characters (likely formatting artifacts)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Keep line if it has reasonable alphanumeric content
        alphanum_chars = sum(c.isalnum() for c in line)
        total_chars = len(line.strip())
        if total_chars > 0 and alphanum_chars / total_chars > 0.3:
            cleaned_lines.append(line.strip())
        # Skip empty lines (don't add them)
    
    text = '\n'.join(cleaned_lines)
    
    return text.strip()