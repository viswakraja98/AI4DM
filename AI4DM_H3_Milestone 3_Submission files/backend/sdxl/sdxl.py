import torch
import torchvision.transforms.functional as TF
from diffusers import (
    AutoencoderKL,
    EulerAncestralDiscreteScheduler,
    StableDiffusionXLAdapterPipeline,
    T2IAdapter,
)
from PIL import Image
import os

import base64
import io

def encode_image(image, format="PNG"):
    with io.BytesIO() as buffer:
        image.save(buffer, format=format)
        return f"data:image/{format};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    adapter = T2IAdapter.from_pretrained(
        "TencentARC/t2i-adapter-sketch-sdxl-1.0", torch_dtype=torch.float16, variant="fp16"
    )
    scheduler = EulerAncestralDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionXLAdapterPipeline.from_pretrained(
        model_id,
        vae=AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16),
        adapter=adapter,
        scheduler=scheduler,
        torch_dtype=torch.float16,
        variant="fp16",
    )
    pipe.to(device)
    generator = torch.Generator(device=device)
else:
    raise Exception("No CUDA Device enabled: SDXL not compatible with non CUDA GPU environment")

def run_model(prompt="Happy Dog in a green park with bushes, playing with a ball", image=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.png'))):
    return encode_image(pipe(
        # prompt=f"cinematic photo {prompt} .35mm photograph, 4k, highly detailed, realistic",
        prompt = prompt,
        # negative_prompt="drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
        negative_prompt="extra digit, fewer digits, cropped, worst quality, low quality, glitch, deformed, mutated, ugly, disfigured",
        image=Image.eval(TF.to_pil_image((TF.to_tensor(image.convert("L").convert("RGB")) > 0.5).to(torch.float32)), lambda x: 255-x),
        num_inference_steps=25,
        generator=generator,
        guidance_scale=5,
        adapter_conditioning_scale=0.8,
        adapter_conditioning_factor=0.8,
    ).images[0])
    
if __name__ == '__main__':
    run_model().save("output.png")