#!/usr/bin/env python3
"""
Dashboard Launcher
Simple script to start the dashboard with proper error handling
"""

import subprocess
import sys
import time
import webbrowser
import os

def start_dashboard():
    """Start the dashboard with error handling"""
    print("🚀 Starting Dubai Schools Accessibility Dashboard...")
    print("=" * 60)
    
    try:
        # Change to the project directory
        os.chdir('/Users/kirannarayana/Desktop/F21RP')
        
        # Start the dashboard
        print("📊 Loading dashboard...")
        process = subprocess.Popen([
            sys.executable, 
            'phase3_dashboard/simple_advanced_dashboard.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        print("⏳ Starting server...")
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Dashboard started successfully!")
            print("🌐 Dashboard URL: http://localhost:8050")
            print("📱 Opening in browser...")
            
            # Open in browser
            webbrowser.open('http://localhost:8050')
            
            print("\n🎯 Dashboard Features:")
            print("  • Interactive maps and charts")
            print("  • 6 analysis tabs")
            print("  • Real-time filtering")
            print("  • Mobile responsive design")
            print("\n🛑 Press Ctrl+C to stop the dashboard")
            
            # Keep the script running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping dashboard...")
                process.terminate()
                print("✅ Dashboard stopped")
        else:
            print("❌ Dashboard failed to start")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error: {stderr.decode()}")
                
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("\n💡 Alternative: Open the static HTML dashboard:")
        print("   open phase3_dashboard/static_dashboard.html")

if __name__ == "__main__":
    start_dashboard()
