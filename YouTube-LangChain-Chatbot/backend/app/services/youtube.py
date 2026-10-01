from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from a YouTube URL.
    """

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]

    raise ValueError("Invalid YouTube URL")


def get_transcript(url: str) -> str:
    """
    Fetch the transcript of a YouTube video.
    """

    video_id = get_video_id(url)

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    text = " ".join(
        snippet.text for snippet in transcript
    )

    return text