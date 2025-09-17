#!/usr/bin/env python3
"""
Interactive Dubai Map Dashboard Launcher
Launches the most sophisticated Dubai-focused dashboard with small points and full interactivity
"""

import subprocess
import sys
import time
import webbrowser
import os

def launch_interactive_dashboard():
    """Launch the interactive Dubai map dashboard"""
    print("🚀 Launching Interactive Dubai Map Dashboard...")
    print("=" * 60)
    
    try:
        # Change to the project directory
        os.chdir('/Users/kirannarayana/Desktop/F21RP')
        
        # Start the interactive dashboard
        print("🎨 Loading interactive Dubai map dashboard...")
        process = subprocess.Popen([
            sys.executable, 
            'phase3_dashboard/advanced_dubai_map_dashboard.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the server to start
        print("⏳ Starting interactive server...")
        time.sleep(8)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Interactive Dubai Map Dashboard launched successfully!")
            print("🌐 Dashboard URL: http://localhost:8053")
            print("📱 Opening in browser...")
            
            # Open in browser
            webbrowser.open('http://localhost:8053')
            
            print("\n🎯 Interactive Dubai Map Dashboard Features:")
            print("  • 🗺️ Dubai-focused map with proper boundaries")
            print("  • 🔍 Small, refined school markers (3-7px)")
            print("  • 🎨 Dark theme with sophisticated styling")
            print("  • 🔍 Advanced filtering system")
            print("  • 📊 Real-time analytics")
            print("  • 📱 Mobile responsive design")
            print("  • 🎭 Modern glassmorphism design")
            print("  • ⚡ Smooth animations and transitions")
            print("  • 🚇 Metro station overlays (8px)")
            print("  • 🏥 Healthcare facility integration")
            
            print("\n🗺️ Map Interactivity:")
            print("  • ✅ Full zoom in/out capability")
            print("  • ✅ Pan and scroll functionality")
            print("  • ✅ Hover tooltips with school details")
            print("  • ✅ Click and drag to navigate")
            print("  • ✅ Mouse wheel zoom")
            print("  • ✅ Touch support for mobile")
            print("  • ✅ Professional map controls")
            
            print("\n🔍 Filter Options:")
            print("  • School Type filtering")
            print("  • Performance Category filtering")
            print("  • Geographic Cluster filtering")
            print("  • Distance range sliders")
            print("  • Urban score range filtering")
            print("  • Real-time map updates")
            
            print("\n🎨 Design Features:")
            print("  • Glassmorphism cards with backdrop blur")
            print("  • Neon color scheme (cyan, green, red, yellow)")
            print("  • Gradient backgrounds")
            print("  • Modern typography (Inter font)")
            print("  • Smooth hover effects")
            print("  • Professional spacing and layout")
            print("  • Dubai-focused map styling")
            print("  • Small, clean markers for better visibility")
            
            print("\n🛑 Press Ctrl+C to stop the dashboard")
            
            # Keep the script running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping interactive Dubai map dashboard...")
                process.terminate()
                print("✅ Dashboard stopped")
        else:
            print("❌ Interactive Dubai map dashboard failed to start")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error: {stderr.decode()}")
                
    except Exception as e:
        print(f"❌ Error launching interactive Dubai map dashboard: {e}")
        print("\n💡 Alternative: Open the static HTML dashboard:")
        print("   open phase3_dashboard/static_dashboard.html")

if __name__ == "__main__":
    launch_interactive_dashboard()
