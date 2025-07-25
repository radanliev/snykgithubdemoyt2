#!/usr/bin/env python3
"""
Demo Repository Launcher
Choose between the security demo app and the weather app
"""

import sys
import subprocess
import os

def print_banner():
    print("=" * 60)
    print("  SNYK GITHUB DEMO REPOSITORY")
    print("=" * 60)
    print()

def show_menu():
    print("Available Applications:")
    print()
    print("1. 🌤️  Weather App")
    print("   - Modern weather application with mock data")
    print("   - Web interface and REST API")
    print("   - Runs on http://localhost:8000")
    print()
    print("2. 🔒 Security Demo App")
    print("   - Flask app with intentional vulnerabilities")
    print("   - For Snyk security scanning demonstration")
    print("   - Runs on http://localhost:5000")
    print()
    print("3. ℹ️  Show Information")
    print("   - Display repository information")
    print()
    print("4. 🚪 Exit")
    print()

def run_weather_app():
    print("Starting Weather App...")
    print("The app will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    try:
        subprocess.run([sys.executable, "weather_app_simple.py"])
    except KeyboardInterrupt:
        print("\nWeather app stopped.")
    except FileNotFoundError:
        print("Error: weather_app_simple.py not found!")

def run_security_demo():
    print("Starting Security Demo App...")
    print("The app will be available at: http://localhost:5000")
    print("⚠️  WARNING: This app contains intentional security vulnerabilities!")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    try:
        subprocess.run([sys.executable, "app2.py"])
    except KeyboardInterrupt:
        print("\nSecurity demo app stopped.")
    except FileNotFoundError:
        print("Error: app2.py not found!")

def show_info():
    print("Repository Information:")
    print("-" * 40)
    print("🌤️  Weather App:")
    print("   - Self-contained Python weather application")
    print("   - No external dependencies required")
    print("   - Mock weather data for 5+ cities")
    print("   - Random weather generation for unknown cities")
    print("   - REST API: GET /api/weather?city=<cityname>")
    print()
    print("🔒 Security Demo:")
    print("   - Flask application with security vulnerabilities")
    print("   - Used for Snyk security scanning demonstrations")
    print("   - Contains: hardcoded credentials, eval(), os.system()")
    print("   - DO NOT use in production!")
    print()
    print("📁 Files:")
    files = [
        "weather_app_simple.py - Weather application",
        "app2.py - Security demo Flask app", 
        "dummy.py - Simple demo function",
        "requirements.txt - Python dependencies",
        "README.md - Documentation"
    ]
    for file in files:
        if os.path.exists(file.split(' - ')[0]):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file}")
    print()

def main():
    print_banner()
    
    while True:
        show_menu()
        try:
            choice = input("Enter your choice (1-4): ").strip()
            print()
            
            if choice == '1':
                run_weather_app()
            elif choice == '2':
                run_security_demo()
            elif choice == '3':
                show_info()
            elif choice == '4':
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
            
            print()
            input("Press Enter to continue...")
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except EOFError:
            break

if __name__ == '__main__':
    main()