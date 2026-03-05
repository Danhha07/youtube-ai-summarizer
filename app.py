from youtube_transcript_api import YouTubeTranscriptApi

video_id = input("Enter YouTube video id: ")

ytt = YouTubeTranscriptApi()

transcript = ytt.fetch(video_id)

text = " ".join([x.text for x in transcript])

print("\nTranscript:\n")
print(text[:1000])
