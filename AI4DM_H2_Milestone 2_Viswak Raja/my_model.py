import requests
import io
from PIL import Image
import os

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        # Check response status and content type
        if response.status_code == 200 and "image" in response.headers["Content-Type"]:
            return response.content
        else:
            print(f"Failed to retrieve image: {response.status_code}")
            print(f"Response content: {response.text}")  # Print the error message
            return None

# Function to query the API with the provided prompt and save the image
def text2img(prompt):
    # Query the image based on the prompt
    image_bytes = query({
        "inputs": prompt,
    })

    if image_bytes:
        try:
            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Define the path to save the image in the static folder
            static_folder = "static"  # Assuming 'static' is the folder where you want to save the image
            os.makedirs(static_folder, exist_ok=True)  # Create the folder if it doesn't exist
            
            # Save the image inside the 'static' folder
            image_path = os.path.join(static_folder, "generated_image.png")
            image.save(image_path)  # Save as PNG or any preferred format
            print(f"Image saved as '{image_path}'")
            return image_path  # Return the image path if needed
        except Exception as e:
            print(f"Error opening or saving image: {e}")
    else:
        print("No valid image data returned.")

import base64
import os
from openai import OpenAI

client = OpenAI()

# Function to encode the image from the static folder
def encode_image(image_name, folder="static"):
    # Build the full image path
    image_path = os.path.join(folder, image_name)
    print(image_path)
    
    # Open and encode the image
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# # Image name and path (assuming the image is saved in the 'static' folder)
# image_name = "generated_image.png"

# # Get the base64 string from the static folder
# base64_image = encode_image(image_name, folder="static")


def generate_story(image_name):
    role = [
        "kid",
        "expert",
        "explaining to a blind person"
    ]
    base64_image = encode_image(image_name, folder="static")
    
# Create the API call to process the image
    completion =  client.chat.completions.create(
        model="gpt-4o-mini",
        max_completion_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    { 
                        "type": "text",
                        "text": "Describe in short what is in this image in four quadrants like "+role[2] +'.',
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"  # Send the image as base64
                        },
                    },
                ],
            }
        ],
    )

    return completion.choices[0].message.content