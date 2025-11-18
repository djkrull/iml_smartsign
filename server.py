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


def convert_timedelta_to_time_str(td_value):
    """Convert timedelta seconds to HH:MM format"""
    if pd.isna(td_value):
        return None

    try:
        # If it's a timedelta object
        if isinstance(td_value, timedelta):
            total_seconds = int(td_value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        # If it's already a string, return as is
        elif isinstance(td_value, str):
            return td_value
        else:
            return None
    except:
        return None


def extract_speaker_from_description(desc_html):
    """Extract speaker from HTML description (format: <b>Speaker</b><br/>Name, Institution<br/>)"""
    if not desc_html or pd.isna(desc_html):
        return ''

    try:
        desc_str = str(desc_html)
        # Look for <b>Speaker</b> tag and extract the following text
        if '<b>Speaker</b>' in desc_str:
            start_idx = desc_str.find('<b>Speaker</b>') + len('<b>Speaker</b>')
            end_idx = desc_str.find('<br/>', start_idx)
            if end_idx == -1:
                end_idx = desc_str.find('<br />', start_idx)
            if end_idx == -1:
                end_idx = start_idx + 200  # Fallback: take next 200 chars

            speaker_text = desc_str[start_idx:end_idx].strip()
            # Remove any remaining HTML tags
            speaker_text = speaker_text.replace('<br/>', '').replace('<br />', '').strip()
            return speaker_text
        else:
            return ''
    except:
        return ''


def process_excel_to_csv(excel_file):
    """Process Excel file and generate CSV - supports both simple and ProjectPlace export formats"""
    try:
        # Read Excel
        xls = pd.ExcelFile(excel_file)

        # Find correct sheet
        sheet_name = None
        for name in ['Data', 'data', 'Seminars', 'seminars', 'Program', 'program', 'ExportedPrograms']:
            if name in xls.sheet_names:
                sheet_name = name
                break

        if sheet_name is None:
            sheet_name = xls.sheet_names[0]

        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        if df.empty:
            return False, "Excel file is empty", 0

        # Detect format (ProjectPlace export vs simple format)
        is_projectplace_format = 'Start date' in df.columns and 'Start time' in df.columns

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

            # Parse date based on format
            if is_projectplace_format:
                date_value = row.get('Start date', None)
            else:
                date_value = row.get('Date', None)

            seminar_date = parse_date(date_value)

            if seminar_date is None:
                continue

            # Check if this week
            if not (week_start <= seminar_date <= week_end):
                continue

            # Parse time based on format
            if is_projectplace_format:
                time_value = convert_timedelta_to_time_str(row.get('Start time', None))
            else:
                time_value = str(row.get('Time', ''))

            # Check if future event
            if time_value and time_value.lower() != 'nan':
                try:
                    start_time_str = time_value.split('-')[0].strip() if '-' in time_value else time_value
                    start_time = pd.to_datetime(start_time_str, format='%H:%M').time()
                    event_datetime = datetime.combine(seminar_date, start_time)
                    if event_datetime < current_time:
                        continue
                except:
                    pass  # If time parsing fails, don't skip the event

            # Extract speaker
            if is_projectplace_format:
                speaker = extract_speaker_from_description(row.get('Description', ''))
            else:
                speaker = row.get('Speaker', '')

            # Get title
            title = row.get('Title', '')

            # Smart parsing: If speaker is empty but title contains "Name: Title" format, parse it
            # e.g., "Genming Bai: TBA" → Speaker="Genming Bai", Title="TBA"
            if (not speaker or str(speaker).strip() == '' or str(speaker).lower() == 'nan') and ':' in str(title):
                parts = str(title).split(':', 1)
                if len(parts) == 2:
                    potential_speaker = parts[0].strip()
                    potential_title = parts[1].strip()

                    # Only parse if left side looks like a person's name (not a course code or long title)
                    # Heuristics:
                    # - Should be relatively short (< 60 chars, typically names are 20-40 chars)
                    # - Should not contain numbers at the start (like "FSF3571")
                    # - Should not contain certain course-like keywords ("course", "lecture", "module", "seminar" in the left part)
                    # - Should not contain slashes or URLs
                    course_keywords = ['course', 'lecture', 'module', 'seminar', 'workshop', 'session', 'tutorial']
                    has_course_keyword = any(keyword in potential_speaker.lower() for keyword in course_keywords)
                    looks_like_code = potential_speaker and potential_speaker[0].isdigit()

                    if (potential_speaker and len(potential_speaker) < 60 and
                        not has_course_keyword and not looks_like_code and
                        not potential_speaker.startswith('http') and '/' not in potential_speaker):
                        speaker = potential_speaker
                        title = potential_title

            # Get location
            if is_projectplace_format:
                location = row.get('Room location', '')
            else:
                location = row.get('Location', '')

            # Add to results
            filtered_rows.append({
                'Title_Original': row.get('Title', ''),
                'Title': title,
                'Speaker': speaker,
                'Date': seminar_date.isoformat(),
                'Date_Formatted': seminar_date.strftime('%A %d %b').capitalize(),
                'Time': time_value if time_value else '',
                'Location': location,
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
