#!/usr/bin/env python3
"""
Futuristic Dashboard Launcher
Launches the most advanced, futuristic dashboard
"""

import subprocess
import sys
import time
import webbrowser
import os

def launch_futuristic_dashboard():
    """Launch the futuristic dashboard"""
    print("🚀 Launching Futuristic Dubai Schools Dashboard...")
    print("=" * 60)
    
    try:
        # Change to the project directory
        os.chdir('/Users/kirannarayana/Desktop/F21RP')
        
        # Start the futuristic dashboard
        print("🎨 Loading futuristic dashboard...")
        process = subprocess.Popen([
            sys.executable, 
            'phase3_dashboard/futuristic_dashboard.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the server to start
        print("⏳ Starting futuristic server...")
        time.sleep(8)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Futuristic Dashboard launched successfully!")
            print("🌐 Dashboard URL: http://localhost:8051")
            print("📱 Opening in browser...")
            
            # Open in browser
            webbrowser.open('http://localhost:8051')
            
            print("\n🎯 Futuristic Dashboard Features:")
            print("  • 🎨 Modern glassmorphism design")
            print("  • 🌟 Neon glow effects and animations")
            print("  • 🗺️ Highly interactive maps")
            print("  • 🔍 Advanced filtering system")
            print("  • 📊 Real-time analytics")
            print("  • 📱 Mobile responsive design")
            print("  • 🎭 Dark theme with futuristic colors")
            print("  • ⚡ Smooth animations and transitions")
            
            print("\n🎨 Design Features:")
            print("  • Glassmorphism cards with backdrop blur")
            print("  • Neon color scheme (cyan, green, red, yellow)")
            print("  • Gradient backgrounds")
            print("  • Modern typography (Inter font)")
            print("  • Smooth hover effects")
            print("  • Professional spacing and layout")
            
            print("\n🔍 Filter Options:")
            print("  • School Type filtering")
            print("  • Performance Category filtering")
            print("  • Geographic Cluster filtering")
            print("  • Distance range sliders")
            print("  • Urban score range filtering")
            print("  • Real-time map updates")
            
            print("\n🛑 Press Ctrl+C to stop the dashboard")
            
            # Keep the script running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping futuristic dashboard...")
                process.terminate()
                print("✅ Dashboard stopped")
        else:
            print("❌ Futuristic dashboard failed to start")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error: {stderr.decode()}")
                
    except Exception as e:
        print(f"❌ Error launching futuristic dashboard: {e}")
        print("\n💡 Alternative: Open the static HTML dashboard:")
        print("   open phase3_dashboard/static_dashboard.html")

if __name__ == "__main__":
    launch_futuristic_dashboard()
