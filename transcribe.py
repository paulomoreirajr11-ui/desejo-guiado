# -*- coding: utf-8 -*-
"""Transcreve o audio do WhatsApp usando faster-whisper (CPU)."""
from faster_whisper import WhisperModel

AUDIO = r"C:\projeto irene moreira\WhatsApp Ptt 2026-06-18 at 14.30.34.ogg"
OUT = r"C:\projeto irene moreira\transcricao_audio.txt"

print("Carregando modelo (baixa na 1a vez)...", flush=True)
model = WhisperModel("small", device="cpu", compute_type="int8")

print("Transcrevendo...", flush=True)
segments, info = model.transcribe(AUDIO, language="pt", beam_size=5, vad_filter=True)

lines = []
for seg in segments:
    lines.append(f"[{seg.start:6.1f}s] {seg.text.strip()}")
text = "\n".join(lines)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(text + "\n")

print(f"DURACAO_AUDIO_S: {round(info.duration, 1)}", flush=True)
print("----- TRANSCRICAO -----", flush=True)
print(text, flush=True)
print("----- FIM -----", flush=True)
