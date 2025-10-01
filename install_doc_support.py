#!/usr/bin/env python3
"""
Script para instalar suporte a arquivos .doc
"""

import subprocess
import sys

def install_doc_support():
    """Instala bibliotecas para suporte a arquivos .doc"""
    try:
        print("Instalando python-docx2txt para suporte a arquivos .doc...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "docx2txt"])
        print("✅ python-docx2txt instalado com sucesso!")
        print("Agora você pode enviar arquivos .doc e .docx")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar python-docx2txt: {e}")
        print("Arquivos .docx ainda funcionarão, mas .doc pode ter limitações")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    install_doc_support()
