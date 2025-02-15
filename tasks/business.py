import os
import requests
import subprocess
import sqlite3
import csv
import json
from bs4 import BeautifulSoup  # make sure to add beautifulsoup4 to requirements.txt
from PIL import Image          # from Pillow
import markdown
import speech_recognition as sr

# --- Task B3: Fetch Data from an API and Save It ---


def task_b3_fetch_data(api_url: str, output_filename: str):
    """
    Fetch data from the provided API URL and save the response to ./data/<output_filename>.
    Security: Only files under ./data are written.
    """
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

    # Ensure output path is under ./data
    output_path = os.path.join("./data", output_filename)
    with open(output_path, "w") as f:
        f.write(response.text)
    return f"Fetched data from {api_url} and saved to {output_filename}"


# --- Task B4: Clone a Git Repo and Make a Commit ---
def task_b4_clone_repo_and_commit(repo_url: str, commit_message: str):
    """
    Clone a git repository into ./data/repo_temp, create a new file, commit it,
    and (optionally) push the commit.
    Security: All operations occur inside ./data.
    """
    import shutil
    clone_dir = os.path.join("./data", "repo_temp")
    # Delete only within ./data (allowed deletion)
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    result = subprocess.run(
        ["git", "clone", repo_url, clone_dir],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception("Failed to clone repository: " + result.stderr)

    new_file_path = os.path.join(clone_dir, "new_file.txt")
    with open(new_file_path, "w") as f:
        f.write("Automated commit by LLM-based Automation Agent")

    subprocess.run(["git", "-C", clone_dir, "add", "new_file.txt"], check=True)
    subprocess.run(["git", "-C", clone_dir, "commit",
                   "-m", commit_message], check=True)

    return f"Cloned repo from {repo_url} and created a commit with message: {commit_message}"


# --- Task B5: Run a SQL Query on a SQLite Database ---
def task_b5_run_sql_query(db_path: str, query: str, output_filename: str):
    """
    Run a SQL query on a SQLite database and write the results to ./data/<output_filename>.
    Security: The provided db_path must be under ./data.
    """
    # Enforce that db_path is under ./data
    if not db_path.startswith("./data"):
        raise Exception("Access to databases outside ./data is not allowed.")

    if not os.path.isfile(db_path):
        raise Exception(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    output_path = os.path.join("./data", output_filename)
    with open(output_path, "w") as f:
        for row in rows:
            f.write(str(row) + "\n")

    return f"Executed SQL query and saved results to {output_filename}"


# --- Task B6: Extract Data from (Scrape) a Website ---
def task_b6_scrape_website(url: str, output_filename: str):
    """
    Scrape the website at the given URL and extract data.
    For example, extract all text from <p> tags.
    Save the result to ./data/<output_filename>.
    Security: Only data under ./data is written.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve website: HTTP {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    output_text = "\n".join(paragraphs)

    output_path = os.path.join("./data", output_filename)
    with open(output_path, "w") as f:
        f.write(output_text)

    return f"Scraped website {url} and saved data to {output_filename}"


# --- Task B7: Compress or Resize an Image ---
def task_b7_resize_image(input_image_path: str, output_image_path: str, size: tuple = (800, 600)):
    """
    Resize the image at input_image_path to the given size and save it to output_image_path.
    Security: Both paths must be under ./data.
    """
    if not input_image_path.startswith("./data") or not output_image_path.startswith("./data"):
        raise Exception("Access only to files under ./data is allowed.")

    if not os.path.isfile(input_image_path):
        raise Exception(f"Image file not found: {input_image_path}")

    with Image.open(input_image_path) as img:
        img_resized = img.resize(size)
        img_resized.save(output_image_path)

    return f"Resized image saved to {output_image_path}"


# --- Task B8: Transcribe Audio from an MP3 File ---
def task_b8_transcribe_audio(audio_path: str, output_filename: str):
    """
    Transcribe an audio file (MP3) and write the transcription to ./data/<output_filename>.
    Security: Only audio files under ./data are accessed.
    """
    if not audio_path.startswith("./data"):
        raise Exception("Access only to files under ./data is allowed.")

    if not os.path.isfile(audio_path):
        raise Exception(f"Audio file not found: {audio_path}")

    recognizer = sr.Recognizer()
    # Depending on your environment, you may need to convert MP3 to WAV first.
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        transcription = recognizer.recognize_google(audio)
    except Exception as e:
        raise Exception("Transcription failed: " + str(e))

    output_path = os.path.join("./data", output_filename)
    with open(output_path, "w") as f:
        f.write(transcription)

    return f"Transcription saved to {output_filename}"


# --- Task B9: Convert Markdown to HTML ---
def task_b9_markdown_to_html(input_md: str, output_html: str):
    """
    Convert the Markdown file at input_md to HTML and save it to output_html.
    Security: Both files must be under ./data.
    """
    if not input_md.startswith("./data") or not output_html.startswith("./data"):
        raise Exception("Access only to files under ./data is allowed.")

    if not os.path.isfile(input_md):
        raise Exception(f"Markdown file not found: {input_md}")

    with open(input_md, "r") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)

    with open(output_html, "w") as f:
        f.write(html_content)

    return f"Converted {input_md} to HTML and saved as {output_html}"


def task_b10_filter_csv(file_path: str, filter_column: str, filter_value: str):
    """
    Filter the CSV file at file_path (which must be under ./data) by matching rows 
    where the value in filter_column equals filter_value.
    Write the filtered rows as JSON into ./data/csv_filtered.json.

    This function enforces that:
      - Only files under ./data are accessed (B1).
      - No files outside are deleted or modified (B2).
    """
    # Ensure file_path is within ./data
    if not file_path.startswith("./data"):
        raise Exception("Access to files outside ./data is not allowed.")

    if not os.path.isfile(file_path):
        raise Exception(f"CSV file not found: {file_path}")

    filtered_rows = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get(filter_column) == filter_value:
                filtered_rows.append(row)

    output_path = "./data/csv_filtered.json"
    with open(output_path, "w") as f:
        json.dump(filtered_rows, f, indent=2)

    return f"Filtered CSV and saved results to {output_path}"
