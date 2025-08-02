import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time
import json
import yt_dlp as youtube_dl

#upload
upload_endpoints = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, chunk_size = 5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoints, headers = headers, data = read_file(filename))
    #print(response.json())

    audio_url = upload_response.json()['upload_url']
    return audio_url

# transcribe
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {"audio_url": audio_url, "sentiment_analysis": sentiment_analysis}
    transcript_response = requests.post(transcript_endpoint, json = transcript_request, headers = headers)
    #print(response.json())
    job_id = transcript_response.json()['id']
    return job_id

#audio_url = upload(filename)
#transcript_id = transcribe(audio_url)

#print(transcript_id)

# poll
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers = headers)
    #print(polling_response.json())
    return polling_response.json()

def get_transcription_result_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while(True):
        data = poll(transcript_id)
        #polling_response = requests.get(polling_endpoint, headers = headers)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        print('Waiting 30 seconds....')
        time.sleep(30)

# save transcript

def save_transcript(audio_url, filename, sentiment_analysis = False):
    data, error = get_transcription_result_url(audio_url, sentiment_analysis)

    if data and data.get("text"):
        text_filename = filename + ".txt"
        with open(f"data/{title}.txt", "w") as f:
            if data and data.get('text'):
                f.write(data['text'])
            else:
                f.write("[ERROR] No transcript text found.")
                print("❌ Transcript returned None or empty.")

        if sentiment_analysis and data.get("sentiment_analysis_results"):
            sentiment_filename = filename + "_sentiment.json"
            with open(sentiment_filename, "w") as f:
                json.dump(data["sentiment_analysis_results"], f, indent=4)

        print("Transcription and sentiment saved.")
    else:
        print("Error: No transcription text found.")
        if error:
            print("AssemblyAI error:", error)
        return False

        if sentiment_analysis:
            text_filename = filename + "_sentiment.json"
            with open(text_filename, "w") as f:
                sentiments = data["sentiment_analysis_results"]
                json.dump(sentiments, f, indent = 4)
            print('Transcription saved')
        elif error:
            print('Error', error)
            return False

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.mp3",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Debugging line
    if not os.path.exists("audio.mp3"):
        print("❌ audio.mp3 not found after download")
    else:
        print("✅ audio.mp3 downloaded")

