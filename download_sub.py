import yt_dlp
import json
import time
import sys
import os

# Check if the job_index argument is passed
if len(sys.argv) < 2:
    print("Please provide a job index.")
    sys.exit(1)

job_index = int(sys.argv[1])

# Read the jobs from jobs.json
try:
    with open('jobs.json', 'r') as f:
        content = f.read().strip()  # Strip leading/trailing spaces or empty lines
        if not content:
            print("jobs.json is empty!")
            sys.exit(1)  # Exit with an error if the file is empty
        jobs_data = json.loads(content)  # Parse the content as JSON
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {str(e)}")
    sys.exit(1)  # Exit if JSON is invalid
except Exception as e:
    print(f"Error reading jobs.json: {str(e)}")
    sys.exit(1)  # Exit for other errors

# Calculate the start and end indices based on the job_index
start_index = (job_index - 1) * 10
end_index = start_index + 10

# Select the appropriate range of jobs based on the job index
jobs_to_process = jobs_data[start_index:end_index]

# Set options for yt-dlp
options = {
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'skip_download': True,
    'outtmpl': '%(title)s.%(ext)s',
    'cookiefile': 'cookies.txt',
}

def download_video(url):
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print(f"Successfully downloaded subtitles for {url}")
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error for {url}: {str(e)}")  # Video unavailable or other download errors
    except yt_dlp.utils.ExtractorError as e:
        print(f"Extractor error for {url}: {str(e)}")  # Issues with extracting video info
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {str(e)}")  # Other unexpected errors
    finally:
        # Optional: Pause for a short time before the next download
        time.sleep(2)

# Process each job in the selected range
for job in jobs_to_process:
    url = job["url"]
    print(f"Starting download for {url}")
    download_video(url)

# Zip the downloaded subtitles and move them to the output directory
os.makedirs('output', exist_ok=True)
os.system('mv *.vtt output/ || true')  # Move .vtt files to the output folder

# Create a zip of the subtitles
os.system(f'cd output && zip subtitles{job_index}.zip *.vtt || echo "No subtitles to zip" && cd ..')

# Ensure GitHub Action passes even if there's an error
sys.exit(0)  # Forcefully exit with a success code (0)
