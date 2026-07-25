from logger import logger
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from constants.constants import languages, transcripts_dir
from utils.video_utils import extract_video_id
from utils.common import create_directories


def extract_transcript(video_url: str):
    """
    Extract transcript from a YouTube video and save it.

    Args:
        video_url (str): YouTube video URL.

    Returns:
        str: Extracted transcript.
    """

    try : 
        yt_api = YouTubeTranscriptApi()

        video_id = extract_video_id(video_url)
        logger.info(f"Video ID extracted: {video_id}")

        fetched_transcript = yt_api.fetch(video_id, languages = languages)  # .fetch() as an instance method so it is mandatory to use it using an object.
        transcript = ' '.join(i.text for i in fetched_transcript)

        # Create output directory
        create_directories(transcripts_dir)
        # Path(self.config.root_dir).mkdir(parents=True, exist_ok=True)

        # Save transcript
        output_file = Path(transcripts_dir[0]) / "transcript.txt"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(transcript)

        logger.info(f"Transcript saved at: {output_file}")


    except TranscriptsDisabled: 
        logger.exception("No Caption available for this video.")
