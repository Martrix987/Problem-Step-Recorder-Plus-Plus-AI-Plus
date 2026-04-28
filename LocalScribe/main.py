import pystray
from PIL import Image
from capture_engine import CaptureEngine
from llm_pipeline import LLMPipeline
from compiler import MarkdownCompiler

class LocalScribeApp:
    def __init__(self):
        self.capture_engine = CaptureEngine()
        self.llm = LLMPipeline()
        self.compiler = MarkdownCompiler()
        self.icon = None

    def start_recording(self, icon, item):
        """Action for the system tray 'Start' button."""
        self.capture_engine.start()

    def stop_and_generate(self, icon, item):
        """
        Action for the system tray 'Stop' button.
        1. Stops the capture engine and gets the folder path.
        2. Passes the folder to the LLM pipeline to get descriptions.
        3. Passes the descriptions to the compiler to build the .md file.
        """
        session_folder = self.capture_engine.stop()
        if not session_folder:
            print("No session folder returned.")
            return

        print(f"Processing session in {session_folder}...")
        steps_data = self.llm.process_session(session_folder)
        
        md_file = self.compiler.generate_markdown(session_folder, steps_data)
        print(f"Documentation generated successfully at: {md_file}")

    def quit_app(self, icon, item):
        self.icon.stop()

    def run_system_tray(self):
        """Creates and runs the pystray system tray icon with a menu."""
        print("Starting LocalScribe...")
        # Create a simple generic image for the tray icon
        image = Image.new('RGB', (64, 64), color=(73, 109, 137))
        
        menu = pystray.Menu(
            pystray.MenuItem('Start Recording', self.start_recording),
            pystray.MenuItem('Stop & Generate SOP', self.stop_and_generate),
            pystray.MenuItem('Quit', self.quit_app)
        )
        
        self.icon = pystray.Icon("LocalScribe", image, "LocalScribe", menu)
        print("-> System tray icon activated! Look for a blue square in your Windows tray (bottom right).")
        print("-> (Note: To force quit if Ctrl+C doesn't work, simply close this terminal window)")
        self.icon.run()

if __name__ == "__main__":
    app = LocalScribeApp()
    app.run_system_tray()
