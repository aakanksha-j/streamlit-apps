import torch
from diffusers import StableDiffusionPipeLine
import streamlit as st

model = "CompVis/stable-diffusion-v1-4"

pipeline = StableDiffusionPipeLine.from_pretrained(
    model, torch_dtype = torch.float32,
    use_auth_token = True)

image_creation_text = ("Whale in ocean during sunrise")
image = pipeline(image_creation_text, guidance_scale = 7.5)['sample'][0]

st.image(image)