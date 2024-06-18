import torch
from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("arpachat/small-stable-diffusion-v0-th-1200-e5-g16-bs16", torch_dtype=torch.float16)

prompt = "a photo of an astronaut riding a horse on mars"
image = pipeline(prompt).images[0]
image.save("output.png")