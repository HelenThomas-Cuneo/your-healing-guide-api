from flask import Blueprint, jsonify, request, send_file
import os
from datetime import datetime

lead_magnet_bp = Blueprint('lead_magnet', __name__)

@lead_magnet_bp.route('/api/lead-magnet/download', methods=['GET'])
def download_13_body_types():
    """Download the 13 Ayurvedic Body Types PDF"""
    try:
        pdf_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'The_13_Ayurvedic_Body_Types.pdf')
        
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'PDF not found'}), 404
            
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='The_13_Ayurvedic_Body_Types.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@lead_magnet_bp.route('/api/lead-magnet/stats', methods=['GET'])
def get_lead_magnet_stats():
    """Get lead magnet download statistics"""
    try:
        # This would typically come from a database
        # For now, return mock data
        stats = {
            'total_downloads': 1247,
            'this_month': 89,
            'conversion_rate': '12.3%',
            'top_source': 'welcome_page'
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
