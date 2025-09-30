#!/usr/bin/env python3
"""
Rotas de usuário do backend Sonhos Lusíadas
"""

from flask import Blueprint, request, jsonify
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """Obtém perfil do usuário."""
    return jsonify({
        'message': 'Perfil do usuário',
        'user': {
            'id': 1,
            'name': 'Usuário Sonhos Lusíadas',
            'email': 'usuario@sonhoslusiadas.com'
        }
    })

@user_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Obtém dados do dashboard."""
    return jsonify({
        'message': 'Dados do dashboard',
        'stats': {
            'total_analyses': 10,
            'total_dreams': 45,
            'favorite_works': ['Os Lusíadas', 'A Divina Comédia']
        }
    })