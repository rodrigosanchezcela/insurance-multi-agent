"""file for project configuration"""
import os

class Config:
    
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY")