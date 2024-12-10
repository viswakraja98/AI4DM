# Use a pipeline as a high-level helper

from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
import os

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-capfilt-large")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-capfilt-large")

def run_model(prompt = "How many apples present in the image?", image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.png'))):
    return processor.decode(model.generate(**processor(image, prompt, return_tensors="pt"))[0], skip_special_tokens=True)

if __name__ == "__main__":
    print(run_model())
