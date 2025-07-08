# PUBLIC_INTERFACE
def transcribe_audio(audio_path: str, model_name="base") -> str:
    """
    Transcribe an audio file using OpenAI Whisper.
    
    Args:
        audio_path (str): Path to the audio file.
        model_name (str): Whisper model to use ("tiny", "base", "small", "medium", "large")
        
    Returns:
        str: Transcribed text.
    """
    try:
        import whisper
    except ImportError:
        # Install if not present
        import subprocess
        subprocess.check_call(['pip', 'install', 'openai-whisper'])
        import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result['text']
