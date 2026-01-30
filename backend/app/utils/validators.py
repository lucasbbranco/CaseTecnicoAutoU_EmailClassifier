"""
Email Validators - Simplified
==============================
Validadores básicos para emails.
Remove validações não utilizadas.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class EmailValidator:
    """Validador básico de emails."""
    
    MIN_TEXT_LENGTH = 10
    MAX_TEXT_LENGTH = 10000
    
    def validate_email_text(self, text: str) -> Dict[str, Any]:
        """
        Valida texto de email antes do processamento.
        
        Args:
            text: Texto do email
            
        Returns:
            Dict com valid e error
        """
        result = {"valid": True, "error": None}
        
        if not text or not text.strip():
            result["valid"] = False
            result["error"] = "O texto do email não pode estar vazio"
            return result
        
        if len(text.strip()) < self.MIN_TEXT_LENGTH:
            result["valid"] = False
            result["error"] = f"O texto deve ter pelo menos {self.MIN_TEXT_LENGTH} caracteres"
            return result
        
        if len(text) > self.MAX_TEXT_LENGTH:
            result["valid"] = False
            result["error"] = f"O texto excede o limite de {self.MAX_TEXT_LENGTH} caracteres"
            return result
        
        return result
