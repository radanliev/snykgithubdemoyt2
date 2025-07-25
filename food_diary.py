#!/usr/bin/env python3
"""
Food Diary Application
A simple command-line application for tracking daily food intake.
Includes optional built-in web server for viewing entries.
"""

from datetime import datetime, date
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# File to store food entries persistently
DATA_FILE = os.path.join(os.path.dirname(__file__), 'food_diary_data.json')

class FoodDiary:
    def __init__(self):
        self.entries = self.load_data()
    
    def load_data(self):
        """Load food entries from JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_data(self):
        """Save food entries to JSON file."""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.entries, f, indent=2)
            return True
        except IOError:
            return False
    
    def get_current_date_str(self):
        """Get current date as string in YYYY-MM-DD format."""
        return date.today().isoformat()
    
    def validate_food_entry(self, food_name, calories, meal_type):
        """Validate food entry data."""
        if not food_name or not food_name.strip():
            return False, "Food name is required"
        
        try:
            calories = int(calories)
            if calories < 0:
                return False, "Calories must be a positive number"
        except (ValueError, TypeError):
            return False, "Calories must be a valid number"
        
        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if meal_type.lower() not in valid_meal_types:
            return False, f"Meal type must be one of: {', '.join(valid_meal_types)}"
        
        return True, None
    
    def add_entry(self, food_name, calories, meal_type, notes=""):
        """Add a new food entry."""
        is_valid, error_message = self.validate_food_entry(food_name, calories, meal_type)
        if not is_valid:
            return False, error_message
        
        entry = {
            'id': len(self.entries) + 1,
            'food_name': food_name.strip(),
            'calories': int(calories),
            'meal_type': meal_type.lower(),
            'notes': notes.strip(),
            'date': self.get_current_date_str(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.entries.append(entry)
        if self.save_data():
            return True, entry
        else:
            return False, "Failed to save data"
    
    def get_entries_by_date(self, date_str=None):
        """Get food entries for a specific date."""
        if date_str is None:
            date_str = self.get_current_date_str()
        
        return [entry for entry in self.entries if entry['date'] == date_str]
    
    def get_all_entries(self):
        """Get all food entries."""
        return self.entries
    
    def get_stats(self):
        """Get overall statistics."""
        if not self.entries:
            return {
                'total_entries': 0,
                'total_calories': 0,
                'average_calories_per_day': 0,
                'days_tracked': 0
            }
        
        total_calories = sum(entry['calories'] for entry in self.entries)
        unique_dates = set(entry['date'] for entry in self.entries)
        days_tracked = len(unique_dates)
        avg_calories_per_day = total_calories / days_tracked if days_tracked > 0 else 0
        
        return {
            'total_entries': len(self.entries),
            'total_calories': total_calories,
            'average_calories_per_day': round(avg_calories_per_day, 2),
            'days_tracked': days_tracked
        }

# Global food diary instance
food_diary = FoodDiary()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for the web interface."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.serve_main_page()
        elif path == '/food/list':
            self.serve_json(food_diary.get_all_entries())
        elif path.startswith('/food/date/'):
            date_str = path.split('/')[-1]
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                entries = food_diary.get_entries_by_date(date_str)
                self.serve_json({
                    'date': date_str,
                    'entries': entries,
                    'total_entries': len(entries),
                    'total_calories': sum(entry['calories'] for entry in entries)
                })
            except ValueError:
                self.send_error(400, "Invalid date format. Use YYYY-MM-DD")
        elif path == '/food/stats':
            self.serve_json(food_diary.get_stats())
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/food/add':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            data = parse_qs(post_data)
            
            # Extract values (parse_qs returns lists)
            food_name = data.get('food_name', [''])[0]
            calories = data.get('calories', [''])[0]
            meal_type = data.get('meal_type', [''])[0]
            notes = data.get('notes', [''])[0]
            
            success, result = food_diary.add_entry(food_name, calories, meal_type, notes)
            
            if success:
                # Redirect back to main page
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(400, result)
        else:
            self.send_error(404, "Not found")
    
    def serve_main_page(self):
        """Serve the main HTML page."""
        today_entries = food_diary.get_entries_by_date()
        total_calories = sum(entry['calories'] for entry in today_entries)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Food Diary</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input, textarea, select {{ width: 100%; padding: 8px; margin-bottom: 10px; box-sizing: border-box; }}
        button {{ background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }}
        button:hover {{ background-color: #45a049; }}
        .entry {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .entry-date {{ font-weight: bold; color: #2c3e50; }}
        .entry-food {{ color: #27ae60; margin: 5px 0; }}
        .entry-calories {{ color: #e74c3c; }}
        .stats {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🍎 Food Diary</h1>
        
        <h2>Add Food Entry</h2>
        <form method="POST" action="/food/add">
            <div class="form-group">
                <label for="food_name">Food Name:</label>
                <input type="text" id="food_name" name="food_name" required>
            </div>
            <div class="form-group">
                <label for="calories">Calories:</label>
                <input type="number" id="calories" name="calories" min="0" required>
            </div>
            <div class="form-group">
                <label for="meal_type">Meal Type:</label>
                <select id="meal_type" name="meal_type" required>
                    <option value="">Select meal type</option>
                    <option value="breakfast">Breakfast</option>
                    <option value="lunch">Lunch</option>
                    <option value="dinner">Dinner</option>
                    <option value="snack">Snack</option>
                </select>
            </div>
            <div class="form-group">
                <label for="notes">Notes (optional):</label>
                <textarea id="notes" name="notes" rows="3"></textarea>
            </div>
            <button type="submit">Add Entry</button>
        </form>

        <h2>Today's Entries</h2>
        """
        
        if today_entries:
            html += f'<div class="stats"><strong>Total Calories Today: {total_calories}</strong></div>'
            for entry in today_entries:
                html += f'''
            <div class="entry">
                <div class="entry-date">{entry['timestamp']}</div>
                <div class="entry-food">🍽️ {entry['food_name']} ({entry['meal_type']})</div>
                <div class="entry-calories">⚡ {entry['calories']} calories</div>
                '''
                if entry['notes']:
                    html += f'<div>📝 {entry["notes"]}</div>'
                html += '</div>'
        else:
            html += '<p>No entries for today yet. Add your first meal above!</p>'
        
        html += '''
        <h2>API Endpoints</h2>
        <ul>
            <li><strong>GET /food/list</strong> - View all entries as JSON</li>
            <li><strong>GET /food/date/YYYY-MM-DD</strong> - View entries for specific date</li>
            <li><strong>GET /food/stats</strong> - View statistics as JSON</li>
            <li><strong>POST /food/add</strong> - Add new food entry</li>
        </ul>
    </div>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_json(self, data):
        """Serve JSON response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        """Override to reduce logging noise."""
        pass

def start_web_server(port=8000):
    """Start the web server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Web server running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

def print_help():
    """Print help information."""
    print("""
Food Diary - Track your daily food intake

Commands:
  add <food_name> <calories> <meal_type> [notes]  - Add a new food entry
  list [date]                                     - List entries (today if no date)
  stats                                           - Show statistics
  server [port]                                   - Start web server (default port 8000)
  help                                           - Show this help

Meal types: breakfast, lunch, dinner, snack
Date format: YYYY-MM-DD

Examples:
  python food_diary.py add "Chicken Salad" 350 lunch "Healthy and filling"
  python food_diary.py list 2024-01-15
  python food_diary.py stats
  python food_diary.py server 9000
    """)

def main():
    """Main command-line interface."""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        if len(sys.argv) < 5:
            print("Error: add command requires food_name, calories, and meal_type")
            print("Usage: add <food_name> <calories> <meal_type> [notes]")
            return
        
        food_name = sys.argv[2]
        calories = sys.argv[3]
        meal_type = sys.argv[4]
        notes = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else ""
        
        success, result = food_diary.add_entry(food_name, calories, meal_type, notes)
        if success:
            print(f"✅ Added: {result['food_name']} ({result['calories']} cal)")
        else:
            print(f"❌ Error: {result}")
    
    elif command == 'list':
        date_str = sys.argv[2] if len(sys.argv) > 2 else None
        entries = food_diary.get_entries_by_date(date_str)
        
        if not entries:
            print(f"No entries found for {date_str or 'today'}")
            return
        
        print(f"\n📅 Food entries for {date_str or 'today'}:")
        print("-" * 50)
        total_calories = 0
        for entry in entries:
            print(f"🍽️  {entry['food_name']} ({entry['meal_type']})")
            print(f"    ⚡ {entry['calories']} calories at {entry['timestamp']}")
            if entry['notes']:
                print(f"    📝 {entry['notes']}")
            print()
            total_calories += entry['calories']
        print(f"📊 Total calories: {total_calories}")
    
    elif command == 'stats':
        stats = food_diary.get_stats()
        print("\n📊 Food Diary Statistics:")
        print("-" * 30)
        print(f"Total entries: {stats['total_entries']}")
        print(f"Total calories: {stats['total_calories']}")
        print(f"Days tracked: {stats['days_tracked']}")
        print(f"Average calories per day: {stats['average_calories_per_day']}")
    
    elif command == 'server':
        port = 8000
        if len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("Invalid port number, using default 8000")
        
        start_web_server(port)
    
    elif command in ['help', '-h', '--help']:
        print_help()
    
    else:
        print(f"Unknown command: {command}")
        print_help()

if __name__ == '__main__':
    main()