import os
import base64
import requests

class LLMPipeline:
    def __init__(self, model_name="gemma4:e4b", api_url="http://localhost:11434/api/generate", context_size=16192):
        self.model_name = model_name
        self.api_url = api_url
        self.context_size = context_size

    def _encode_image(self, image_path: str) -> str:
        """Reads an image from disk and returns a base64 encoded string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _batch_images(self, image_folder: str, batch_size: int = 5) -> list:
        """
        Scans the session folder for .png files, sorts them, 
        and groups them into manageable batches to prevent VRAM crashes.
        """
        images = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
        batches = [images[i:i + batch_size] for i in range(0, len(images), batch_size)]
        return batches

    def process_session(self, session_folder: str) -> list:
        """
        Takes the session folder, batches the images, sends them to Ollama,
        and returns a list of dictionaries containing the step number, image path, 
        and generated text.
        """
        steps_data = []
        batches = self._batch_images(session_folder)
        step_number = 1
        
        system_prompt = "You are a helpful technical writing assistant. Your task is to extract a concise, single-sentence instruction for what the user is doing in the provided screenshot. Only provide the sentence, nothing else."

        for batch in batches:
            for image_name in batch:
                image_path = os.path.join(session_folder, image_name)
                encoded_image = self._encode_image(image_path)
                
                payload = {
                    "model": self.model_name,
                    "prompt": system_prompt,
                    "images": [encoded_image],
                    "stream": False,
                    "options": {
                        "num_ctx": self.context_size
                    }
                }
                
                try:
                    response = requests.post(self.api_url, json=payload)
                    response.raise_for_status()
                    generated_text = response.json().get('response', '').strip()
                except Exception as e:
                    generated_text = f"Failed to generate description: {e}"
                
                steps_data.append({
                    "step_number": step_number,
                    "image_name": image_name,
                    "description": generated_text
                })
                
                step_number += 1
                
        return steps_data
