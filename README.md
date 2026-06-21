# yt_downloader

## Codex's fix on the Grok initial's implementation.
The video downloader now checks whether ffmpeg is installed. If it is missing, it falls back to the best single-file video stream with both video and audio, so that YouTube link should no longer abort with the merge error. Audio-only downloads also now skip conversion when ffmpeg is unavailable.
