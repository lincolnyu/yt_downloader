import yt_dlp
import sys
import os
import shutil
from typing import Optional


def has_ffmpeg() -> bool:
    """Return True when ffmpeg is available on PATH."""
    return shutil.which("ffmpeg") is not None

def list_formats(url: str):
    """List available formats for the video"""
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"\nTitle: {info.get('title')}")
        print(f"Duration: {info.get('duration_string', 'N/A')}")
        print("\nAvailable formats:")
        formats = info.get('formats', [])
        # Filter to show useful video + audio formats
        for f in formats:
            if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                resolution = f.get('resolution') or f"{f.get('height')}p"
                ext = f.get('ext')
                format_id = f.get('format_id')
                print(f"  {format_id}: {resolution} - {ext} - {f.get('format_note', '')}")

def download_video(url: str, resolution: Optional[str] = None, output_dir: str = "Downloads"):
    """Download YouTube video with options"""
    os.makedirs(output_dir, exist_ok=True)
    ffmpeg_available = has_ffmpeg()
    
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
    }
    
    if ffmpeg_available:
        ydl_opts['merge_output_format'] = 'mp4'  # Best compatibility
        if resolution:
            # Download specific resolution (best video + best audio)
            ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'
        else:
            # Default: highest quality available
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
    else:
        print("ffmpeg is not installed; downloading the best single-file video available.")
        print("Install ffmpeg to download and merge higher-quality video/audio streams.")
        if resolution:
            ydl_opts['format'] = f'best[vcodec!=none][acodec!=none][height<={resolution}]/best[vcodec!=none][acodec!=none]'
        else:
            ydl_opts['format'] = 'best[vcodec!=none][acodec!=none]'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading: {url}")
        ydl.download([url])
        print("Download completed!")

def download_audio_only(url: str, output_dir: str = "Downloads"):
    """Download original/best quality audio only"""
    os.makedirs(output_dir, exist_ok=True)
    ffmpeg_available = has_ffmpeg()
    
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',  # Pure original/best audio
        'quiet': False,
    }

    if ffmpeg_available:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',  # or 'mp3', 'opus', etc.
            'preferredquality': '0',  # Best quality
        }]
    else:
        print("ffmpeg is not installed; downloading the best original audio file without conversion.")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio only: {url}")
        ydl.download([url])
        print("Audio download completed!")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python yt_downloader.py <youtube_url> [resolution]")
        print("  python yt_downloader.py --list <youtube_url>")
        print("  python yt_downloader.py --audio <youtube_url>")
        print("\nExamples:")
        print("  python yt_downloader.py https://youtu.be/VIDEO_ID")
        print("  python yt_downloader.py https://youtu.be/VIDEO_ID 1080")
        print("  python yt_downloader.py --list https://youtu.be/VIDEO_ID")
        print("  python yt_downloader.py --audio https://youtu.be/VIDEO_ID")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == '--list':
        list_formats(sys.argv[2])
    elif arg == '--audio':
        download_audio_only(sys.argv[2])
    else:
        url = arg
        resolution = sys.argv[2] if len(sys.argv) > 2 else None
        download_video(url, resolution)

if __name__ == "__main__":
    main()
