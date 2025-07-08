import os
import tempfile
import yt_dlp

# PUBLIC_INTERFACE
def download_youtube_audio(youtube_url: str, output_format='wav') -> str:
    """
    Download the audio from a YouTube URL and save as a local .wav file.
    
    Args:
        youtube_url (str): The URL of the YouTube video.
        output_format (str): File format to save (default: 'wav').
    
    Returns:
        str: Path to the downloaded audio file.
    """
    tmpdir = tempfile.mkdtemp()
    output_path = os.path.join(tmpdir, "audio.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    # Find output file
    for fname in os.listdir(tmpdir):
        if fname.endswith(f".{output_format}"):
            return os.path.join(tmpdir, fname)
    raise RuntimeError("Audio file not found after yt-dlp download")
