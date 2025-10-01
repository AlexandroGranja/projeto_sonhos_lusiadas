#!/usr/bin/env python3
"""
Aplicação principal do backend Sonhos Lusíadas
"""

import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sonhos-lusiadas-secret-key-2024')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_FILE_SIZE'] = int(os.getenv('MAX_FILE_SIZE', 16777216))  # 16MB

# Configuração do CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173,http://192.168.1.14:5173').split(',')
CORS(app, origins=cors_origins)

# Importa e registra blueprints
try:
    from routes.analysis import analysis_bp
    from routes.user import user_bp
    
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    print("OK: Blueprints registrados com sucesso!")
    
except ImportError as e:
    print(f"ERRO: Erro ao importar blueprints: {e}")
    print("Criando rotas básicas...")
    
    @app.route('/api/analysis/health')
    def health_check():
        return {
            'status': 'ok',
            'message': 'Backend Sonhos Lusíadas funcionando!',
            'version': '1.0.0'
        }

# Rota para servir arquivos estáticos
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos."""
    return send_from_directory('static', filename)

# Rota principal
@app.route('/')
def index():
    """Página principal da API."""
    return {
        'message': 'API Sonhos Lusíadas',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/analysis/health',
            'upload': '/api/analysis/upload',
            'preprocess': '/api/analysis/preprocess',
            'expand-semantic': '/api/analysis/expand-semantic',
            'analyze-contexts': '/api/analysis/analyze-contexts',
            'classify-context': '/api/analysis/classify-context',
            'visualize': '/api/analysis/visualize',
            'download': '/api/analysis/download',
            'complete-analysis': '/api/analysis/complete-analysis'
        }
    }

if __name__ == '__main__':
    # Cria pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configuração de debug
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("INICIANDO: Servidor Sonhos Lusíadas...")
    print(f"UPLOAD: Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"DEBUG: Debug mode: {debug}")
    print(f"CORS: CORS origins: {cors_origins}")
    
    # Inicia o servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug,
        threaded=True,
        use_reloader=False
    )