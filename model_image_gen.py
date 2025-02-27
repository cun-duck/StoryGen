import streamlit
from streamlit import st
from huggingface_hub import InferenceClient
from PIL import Image
import time
from dotenv import load_dotenv
import os

HF_TOKEN_IMAGE_GEN = st.secrets.get("HF_TOKEN_IMAGE_GEN")

STYLE_PROMPT_ENHANCEMENTS = {
    "Pixar Cartoon Style": "3D Pixar cartoon style, reflecting wonder and joy, a playful, adventures.colorful.",
    "Hyper Realism style": "hyperrealistic portrait style, photorealistic detail, 4k, RAW quality,detailed textures.",
    "Manga Style": "japanese Manga Style, Black and White Color, sharp lines, detailed shading,hard brush, No Color, Gray Scale.",
    "Anime Style": "japanese Cartoon Style, vibrant colors, smooth shading, detailed background,expressive eyes,",
    "3D rendered style": "3D rendered style, octane render, realistic lighting, detailed textures.Deep shadows.",
    "Deep Fantasy Style": "Deep Fantasy Style, magical, ethereal, intricate details, dramatic lighting,dreamlike."
}

def generate_image_from_prompt(prompt, hf_token_image_gen=None, image_style="Pixar Cartoon Style"):
    client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token_image_gen or os.environ.get("HF_TOKEN_IMAGE_GEN")
    )

    style_enhancement = STYLE_PROMPT_ENHANCEMENTS.get(image_style, "")

    full_prompt = f"{prompt}, {style_enhancement} in {image_style}"

    try:
        image = client.text_to_image(
            full_prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )
        print(f"Debug (model_image_gen): Type of image object from client.text_to_image: {type(image)}") # Debug: Print image object type

        if image: # Check if image is not None before saving - IMPORTANT
            test_save_path = "test_image_gen_output.png" # Fixed filename for testing
            image.save(test_save_path) # Save image directly in model_image_gen
            print(f"Debug (model_image_gen): Image saved locally at: {test_save_path}") # Debug: Confirmation message
        else:
            print("Debug (model_image_gen): Image object is None, cannot save.")


        return image
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


if __name__ == '__main__':
    contoh_prompt = "A majestic elephant in a jungle"
    contoh_style = "Manga Style"

    generated_image = generate_image_from_prompt(contoh_prompt, image_style=contoh_style)

    if generated_image:
        generated_image.save("contoh_gambar.png")
        print("Gambar berhasil disimpan sebagai contoh_gambar.png")
    else:
        print("Gagal menghasilkan gambar.")
