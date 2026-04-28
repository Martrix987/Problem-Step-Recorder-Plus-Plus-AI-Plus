import os

class MarkdownCompiler:
    @staticmethod
    def generate_markdown(session_folder: str, steps_data: list, title: str = "LocalScribe SOP"):
        """
        Takes the list of generated steps from the LLMPipeline and formats them 
        into a clean Markdown file saved inside the session_folder.
        
        Output format example:
        ### Step 1
        Click on the 'Network' tab in the GUI.
        ![Step 1 Image](step_01.png)
        """
        md_file_path = os.path.join(session_folder, "SOP.md")
        
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            
            for step in steps_data:
                f.write(f"### Step {step['step_number']}\n")
                f.write(f"{step['description']}\n")
                f.write(f"![Step {step['step_number']} Image]({step['image_name']})\n\n")
                
        return md_file_path
