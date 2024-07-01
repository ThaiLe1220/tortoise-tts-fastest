import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices
import os
import shutil
import time

# Measure the time to load the TextToSpeech model
start_time = time.time()
tts = TextToSpeech()
tts_vi = TextToSpeech(lang="vi")
end_time = time.time()
print(
    f"[WORKFLOW] Runtime for loading TextToSpeech model: {end_time - start_time:.4f} seconds\n"
)


def list_voices():
    """List all available voices."""
    start_time = time.time()
    available_voices = os.listdir("tortoise/voices")
    print("Available voices:", available_voices)
    end_time = time.time()
    print(f"[WORKFLOW] Runtime for list_voices: {end_time - start_time:.4f} seconds")


def generate_speech(tts_model, text, voice, preset, output_file):
    """Generate speech using the specified voice and text."""
    start_time = time.time()
    voice_samples, conditioning_latents = load_voice(voice)
    gen = tts_model.tts_with_preset(
        text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset=preset,
    )
    torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
    print(f"Audio saved as '{output_file}'")
    end_time = time.time()
    print(
        f"[WORKFLOW] Runtime for generate_speech: {end_time - start_time:.4f} seconds"
    )
    return output_file


def generate_random_speech(tts_model, text, preset, output_file):
    """Generate speech using a random voice."""
    start_time = time.time()
    gen = tts_model.tts_with_preset(
        text, voice_samples=None, conditioning_latents=None, preset=preset
    )
    torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
    print(f"Audio saved as '{output_file}'")
    end_time = time.time()
    print(
        f"[WORKFLOW] Runtime for generate_random_speech: {end_time - start_time:.4f} seconds"
    )
    return output_file


def upload_custom_voice(custom_voice_folder, file_paths):
    """Upload custom voice files to the specified folder."""
    start_time = time.time()
    os.makedirs(custom_voice_folder, exist_ok=True)
    for i, file_path in enumerate(file_paths):
        shutil.copy(file_path, os.path.join(custom_voice_folder, f"{i}.wav"))
    end_time = time.time()
    print(
        f"[WORKFLOW] Runtime for upload_custom_voice: {end_time - start_time:.4f} seconds"
    )


def generate_custom_voice_speech(
    tts_model, text, custom_voice_name, preset, output_file
):
    """Generate speech using the custom voice."""
    start_time = time.time()
    custom_voice_folder = f"tortoise/voices/{custom_voice_name}"
    voice_samples, conditioning_latents = load_voice(custom_voice_name)
    gen = tts_model.tts_with_preset(
        text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset=preset,
    )
    torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
    print(f"Audio saved as '{output_file}'")
    end_time = time.time()
    print(
        f"[WORKFLOW] Runtime for generate_custom_voice_speech: {end_time - start_time:.4f} seconds"
    )
    return output_file


def combine_voices_and_generate_speech(tts_model, text, voices, preset, output_file):
    """Combine multiple voices and generate speech."""
    start_time = time.time()
    voice_samples, conditioning_latents = load_voices(voices)
    gen = tts_model.tts_with_preset(
        text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset=preset,
    )
    torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
    print(f"Audio saved as '{output_file}'")
    end_time = time.time()
    print(
        f"[WORKFLOW] Runtime for combine_voices_and_generate_speech: {end_time - start_time:.4f} seconds"
    )
    return output_file


def main():
    # Example text and preset
    text = "Joining two modalities results in a surprising increase in generalization! What would happen if we combined them all?"
    # Use tts as usual
    text_vi = "Xin chào, đây là một ví dụ."
    preset = "ultra_fast"  # @param ["ultra_fast", "fast", "standard", "high_quality"]

    # Generate speech with a specific voice
    voice = "train_dotrice"
    generate_speech(tts, text, voice, preset, "output/generated.wav")
    generate_speech(tts_vi, text_vi, voice, preset, "output/generated_vi.wav")

    # Generate speech with a random voice
    generate_random_speech(tts, text, preset, "output/generated_random.wav")
    generate_random_speech(tts_vi, text_vi, preset, "output/generated_random_vi.wav")

    # # Upload and use custom voice
    # CUSTOM_VOICE_NAME = "custom"
    # custom_voice_folder = f"tortoise/voices/{CUSTOM_VOICE_NAME}"
    # simulate_file_upload(["path/to/your/voice1.wav", "path/to/your/voice2.wav"])
    # generate_custom_voice_speech(text, CUSTOM_VOICE_NAME, preset)

    # Combine multiple voices and generate speech
    # combined_voices = ["pat", "william"]
    # combine_voices_and_generate_speech(
    #     tts,
    #     "They used to say that if man was meant to fly, he’d have wings. But he did fly. He discovered he had to.",
    #     combined_voices,
    #     preset,
    #     "output/generated_combined.wav",
    # )


def simulate_file_upload(file_paths):
    """Simulate uploading custom voice files (Replace with your own file paths)."""
    CUSTOM_VOICE_NAME = "custom"
    custom_voice_folder = f"tortoise/voices/{CUSTOM_VOICE_NAME}"
    os.makedirs(custom_voice_folder, exist_ok=True)
    for i, file_path in enumerate(file_paths):
        shutil.copy(file_path, os.path.join(custom_voice_folder, f"{i}.wav"))


if __name__ == "__main__":
    main()
