import streamlit as st
import importlib
from model_text_gen import generate_story_content, parse_story_output
from model_image_gen import generate_image_from_prompt
import time
from PIL import Image
from dotenv import load_dotenv
import os
import langdetect

HF_TOKEN_IMAGE_GEN = st.secrets.get("HF_TOKEN_IMAGE_GEN")
HF_TOKEN_TEXT_GEN = st.secrets.get("HF_TOKEN_TEXT_GEN")


st.markdown(
    """
    <style>
    .centered-header {
        color: gray;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

IMAGE_STYLES = [
    "Pixar Cartoon Style",
    "Hyper Realism style",
    "Manga Style",
    "Anime Style",
    "3D rendered style",
    "Deep Fantasy Style"
]

st.title("Storyboard Generator")

st.sidebar.header(" 🛠️ Pengaturan")

story_idea = st.sidebar.text_area("💭", "Petualangan Semut")

num_scenes = st.sidebar.slider("🎞️ Jumlah Scenes", 1, 10, 3)

image_style = st.sidebar.selectbox("😎 Image Style", IMAGE_STYLES)

if st.sidebar.button("Create Storyboard"):
    if not story_idea:
        st.warning("Please enter a story idea.")
    else:
        with st.spinner("Masak Aer....."):
            try:
                try:
                    user_language = langdetect.detect(story_idea)
                except langdetect.LangDetectException:
                    user_language = "en"

                scenes_data = model_text_gen.generate_story_content(
                    story_idea, num_scenes, HF_TOKEN_TEXT_GEN, user_language=user_language
                )
                st.session_state['scenes_data'] = scenes_data

                generated_images = []
                for i, scene in enumerate(scenes_data):
                    image = model_image_gen.generate_image_from_prompt(
                        scene['prompt'], HF_TOKEN_IMAGE_GEN, image_style
                    )
                    print(f"Debug: Image object type for scene {i+1} from model_image_gen: {type(image)}") 
                    generated_images.append(image)
                    time.sleep(3)

                st.session_state['generated_images'] = generated_images
                st.session_state['images_generated'] = True

                print(f"Debug: Contents of generated_images list: {generated_images}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state['scenes_data'] = None
                st.session_state['generated_images'] = None
                st.session_state['images_generated'] = False


if 'scenes_data' in st.session_state and st.session_state['scenes_data']:
    scenes_data = st.session_state['scenes_data']

st.markdown("<h1 class='centered-header'>Storyboard Dashboard</h1>", unsafe_allow_html=True)

    if 'generated_images' in st.session_state and st.session_state['images_generated']:
        generated_images = st.session_state['generated_images']

        for i, scene in enumerate(scenes_data):
            st.subheader(f"Scene {i+1}")
            col_narasi, col_gambar = st.columns(2)

            with col_narasi:
                st.write(scene['narasi'])

            with col_gambar:
                if generated_images[i]:
                    st.image(generated_images[i], caption=f"Scene {i+1} Image", use_container_width=True)
                else:
                    st.error("Failed to generate image for this scene.")
