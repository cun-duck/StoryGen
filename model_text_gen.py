from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

HF_TOKEN_TEXT_GEN = st.secrets.get("HF_TOKEN_TEXT_GEN", os.getenv("HF_TOKEN_TEXT_GEN"))

def generate_story_content(story_idea, num_scenes, hf_token_text_gen=None, user_language="en"):
    client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token_text_gen or os.environ.get("HF_TOKEN_TEXT_GEN")
    )

    messages = [
        {
            "role": "user",
            "content": f"""Create an adventure story with the story idea: "{story_idea}".
This story must consist of {num_scenes} scenes.
For each scene, provide the output in the following format:

=== SCENE [scene number] ===
**Narration:** [scene narration]
**Image Prompt:** [prompt to generate scene image,make sure that every detail in the scene is translated into a text to image prompt]

Ensure separate output for each scene with the format above."""
        }
    ]

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=1500,
    )

    output_text = completion.choices[0].message.content
    scenes = parse_story_output(output_text)

    return scenes


def parse_story_output(output_text):
    scenes = []
    scene_blocks = output_text.split("=== SCENE ")[1:]

    for scene_block in scene_blocks:
        lines = scene_block.split('\n')
        scene_num = lines[0].split(' ')[0]
        narasi = ""
        prompt = ""
        mode = ""

        for line in lines[1:]:
            if line.startswith("**Narration:**"):
                mode = "narasi"
                narasi += line[len("**Narration:**"):].strip()
            elif line.startswith("**Image Prompt:**"):
                mode = "prompt"
                prompt += line[len("**Image Prompt:**"):].strip()
            elif mode == "narasi":
                narasi += " " + line.strip()
            elif mode == "prompt":
                prompt += " " + line.strip()

        scenes.append({'narasi': narasi.strip(), 'prompt': prompt.strip()})

    return scenes


if __name__ == '__main__':
    contoh_ide_cerita = "A little child gets lost in a magical forest and meets a fairy"
    jumlah_scene = 3
    daftar_scene = generate_story_content(contoh_ide_cerita, jumlah_scene)

    for scene in daftar_scene:
        print(f"Narasi Scene {daftar_scene.index(scene) + 1}:\n{scene['narasi']}\n")
        print(f"Prompt Scene {daftar_scene.index(scene) + 1}:\n{scene['prompt']}\n")
        print("-" * 30)
