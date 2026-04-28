import os
import subprocess
import glob

class CaptureEngine:
    def __init__(self):
        self.is_recording = False
        self.process = None
        
        # Get the path to the user's Pictures/Screenshots directory
        # PSR++.ps1 saves files here by default
        user_profile = os.environ.get("USERPROFILE", "")
        self.screenshots_dir = os.path.join(user_profile, "Pictures", "Screenshots")

    def start(self):
        print("Starting PSR++...")
        
        # Look for the PSR++.ps1 script in the parent directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        psr_script_path = os.path.join(os.path.dirname(script_dir), "PSR++.ps1")
        
        if not os.path.exists(psr_script_path):
            print(f"Error: Could not find {psr_script_path}")
            return
            
        self.is_recording = True
        
        # Launch PSR++.ps1 in the background without blocking the UI
        self.process = subprocess.Popen([
            "powershell.exe", 
            "-ExecutionPolicy", "Bypass", 
            "-File", psr_script_path
        ])

    def stop(self) -> str:
        print("Capture stopped. Locating the most recent session folder...")
        self.is_recording = False
        
        if self.process:
            # Terminate the application gracefully if it's still running
            self.process.terminate()
            self.process = None
            
        # Find the most recently created session folder in the screenshots directory
        if not os.path.exists(self.screenshots_dir):
            print(f"Screenshots directory not found: {self.screenshots_dir}")
            return None
            
        # Get all subdirectories in the Screenshots folder
        subfolders = [f.path for f in os.scandir(self.screenshots_dir) if f.is_dir()]
        
        if not subfolders:
            print(f"No session folders found in {self.screenshots_dir}")
            return None
            
        # Find the most recently modified/created folder
        latest_folder = max(subfolders, key=os.path.getctime)
        print(f"Discovered session folder: {latest_folder}")
        
        return latest_folder
