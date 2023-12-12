import torch
import sounddevice as sd
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan

device = "cuda:0" if torch.cuda.is_available() else "cpu"
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

from datasets import load_dataset

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

def synthesise(text):
    inputs = processor(text=text, return_tensors="pt")
    speech = model.generate_speech(
        inputs["input_ids"].to(device), speaker_embeddings.to(device), vocoder=vocoder
    )

    return speech.cpu().numpy()


def play_synthesized_audio(audio):
    sd.play(audio,samplerate = 16000)
    sd.wait()
    return

def play_text(text):
    audio_numpy = synthesise(text)
    play_synthesized_audio(audio_numpy)
