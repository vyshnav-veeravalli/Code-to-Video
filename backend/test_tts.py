from utils.tts_engine import synthesize_text_to_wav, get_audio_duration_ms

wav_path = synthesize_text_to_wav("Hello, this is your offline code narration test.")
print("Generated:", wav_path)
print("Duration (ms):", get_audio_duration_ms(wav_path))
