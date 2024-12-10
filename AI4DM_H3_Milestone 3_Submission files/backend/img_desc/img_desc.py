import base64
import os
from openai import OpenAI
import io
from PIL import Image

client = OpenAI()

def encode_image(image, format="PNG"):
    with io.BytesIO() as buffer:
        image.save(buffer, format=format)
        return f"data:image/{format};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

def run_model(image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.png'))):
    completion =  client.chat.completions.create(
        model="gpt-4o-mini",
        max_completion_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    { 
                        "type": "text",
                        "text": "Describe in short what is in this image like explaining to a blind person.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encode_image(image)
                        },
                    },
                ],
            }
        ],
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    print(run_model())