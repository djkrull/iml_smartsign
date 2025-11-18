#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartSign Server - Display & Admin Upload
Serves display template, CSV data, and admin upload interface
Optimized for Railway deployment
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, send_file, request, jsonify
import pandas as pd

app = Flask(__name__)
BASE_DIR = Path(__file__).parent


def get_current_week_start():
    """Get Monday of current week"""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return monday.date()


def get_current_week_end():
    """Get Sunday of current week"""
    start = get_current_week_start()
    return start + timedelta(days=6)


def parse_date(date_value):
    """Parse date from various formats"""
    if pd.isna(date_value):
        return None

    if isinstance(date_value, str):
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d']:
            try:
                return pd.to_datetime(date_value, format=fmt).date()
            except:
                continue
        try:
            return pd.to_datetime(date_value).date()
        except:
            return None
    else:
        try:
            return pd.to_datetime(date_value).date()
        except:
            return None


def process_excel_to_csv(excel_file):
    """Process Excel file and generate CSV"""
    try:
        # Read Excel
        xls = pd.ExcelFile(excel_file)

        # Find correct sheet
        sheet_name = None
        for name in ['Data', 'data', 'Seminars', 'seminars', 'Program', 'program']:
            if name in xls.sheet_names:
                sheet_name = name
                break

        if sheet_name is None:
            sheet_name = xls.sheet_names[0]

        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        if df.empty:
            return False, "Excel file is empty", 0

        # Filter seminars
        week_start = get_current_week_start()
        week_end = get_current_week_end()
        filtered_rows = []
        current_time = datetime.now()

        for idx, row in df.iterrows():
            # Check for "website" tag
            tags = str(row.get('Tag(s)', '') or '')
            if 'website' not in tags.lower():
                continue

            # Parse date
            date_value = row.get('Date', None)
            seminar_date = parse_date(date_value)

            if seminar_date is None:
                continue

            # Check if this week
            if not (week_start <= seminar_date <= week_end):
                continue

            # Check if future event
            time_value = str(row.get('Time', ''))
            if time_value and time_value.lower() != 'nan':
                try:
                    start_time_str = time_value.split('-')[0].strip()
                    start_time = pd.to_datetime(start_time_str, format='%H:%M').time()
                    event_datetime = datetime.combine(seminar_date, start_time)
                    if event_datetime < current_time:
                        continue
                except:
                    pass

            # Add to results
            filtered_rows.append({
                'Title_Original': row.get('Title', ''),
                'Title': row.get('Title', ''),
                'Speaker': row.get('Speaker', ''),
                'Date': seminar_date.isoformat(),
                'Date_Formatted': seminar_date.strftime('%A %d %b').capitalize(),
                'Time': row.get('Time', ''),
                'Location': row.get('Location', ''),
            })

        if not filtered_rows:
            return False, "No seminars found tagged with 'website' for this week", 0

        # Generate CSV
        csv_df = pd.DataFrame(filtered_rows)
        csv_path = BASE_DIR / 'seminarier.csv'
        csv_df.to_csv(csv_path, index=False, encoding='utf-8')

        return True, f"Successfully processed {len(filtered_rows)} seminars", len(filtered_rows)

    except Exception as e:
        return False, f"Error processing file: {str(e)}", 0


@app.route('/')
def index():
    """Serve display template"""
    return send_file('template_simple.html', mimetype='text/html')


@app.route('/admin')
def admin():
    """Serve admin upload page"""
    return send_file('admin.html', mimetype='text/html')


@app.route('/seminarier.csv')
def serve_csv():
    """Serve CSV data file"""
    try:
        return send_file('seminarier.csv', mimetype='text/csv')
    except FileNotFoundError:
        return "CSV file not found", 404


@app.route('/<filename>')
def serve_static(filename):
    """Serve static files (images, etc)"""
    # Security: only serve expected file types
    if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return "File not found", 404

    try:
        return send_file(filename, mimetype='image/png' if filename.endswith('.png') else 'image/jpeg')
    except FileNotFoundError:
        return "File not found", 404


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle Excel file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate file type
    if not file.filename.lower().endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Invalid file type. Please upload Excel (.xlsx or .xls)'}), 400

    # Validate file size (10MB)
    if len(file.read()) > 10 * 1024 * 1024:
        return jsonify({'error': 'File is too large. Maximum size is 10MB'}), 400

    file.seek(0)  # Reset file pointer

    try:
        # Process Excel file
        success, message, count = process_excel_to_csv(file)

        if not success:
            return jsonify({'error': message}), 400

        # Success!
        return jsonify({
            'success': True,
            'message': f'Successfully updated with {count} seminars! Display will refresh within 2 minutes.'
        }), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'SmartSign Server'})


@app.before_request
def before_request():
    """Log incoming requests"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.method} {request.path}")


def run_server():
    """Start the server"""
    port = int(os.environ.get('PORT', 8080))

    print("=" * 80)
    print("SMARTSIGN - DISPLAY & ADMIN SERVER (Flask)")
    print("=" * 80)
    print(f"Server running on port {port}")
    print(f"Display template: http://localhost:{port}/")
    print(f"Admin upload:     http://localhost:{port}/admin")
    print(f"CSV data:         http://localhost:{port}/seminarier.csv")
    print(f"Health check:     http://localhost:{port}/health")
    print("=" * 80)

    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)


if __name__ == "__main__":
    run_server()
