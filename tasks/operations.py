import os
import json
import re
import subprocess
import sqlite3
from datetime import datetime
from glob import glob
from pathlib import Path
from dateutil.parser import parse

import requests
import numpy as np

# ---------------------------
# Task A1: Run datagen.py
# ---------------------------


def task_a1_run_datagen(email: str):
    """
    Delete the existing data folder (if any) and run datagen.py with the given email and --root ./data.
    This ensures fresh data is generated each time.
    """
    data_dir = "./data"
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        print(f"Deleted existing data folder: {data_dir}")

    # Run datagen.py with the email and --root ./data arguments.
    result = subprocess.run(
        ["python3", "datagen.py", email, "--root", "./data"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception("Running datagen.py failed: " + result.stderr)

    print(result.stdout)
    return f"datagen.py ran with email {email}"


# ---------------------------
# Task A2: Format markdown file using prettier
# ---------------------------
def task_a2_format_markdown():
    """
    Format the contents of ./data/format.md using prettier@3.4.2,
    updating the file in-place.
    """
    file_path = "./data/format.md"
    if not os.path.isfile(file_path):
        raise Exception(f"File not found: {file_path}")
    result = subprocess.run(
        ["npx", "prettier@3.4.2", "--write", file_path],
        capture_output=True,
        text=True,
        shell=True
    )
    if result.returncode != 0:
        raise Exception("Prettier formatting failed: " + result.stderr)
    return "Formatted markdown using prettier@3.4.2"


# ---------------------------
# Task A3: Count Wednesdays in dates.txt
# ---------------------------
def task_a3_count_wednesdays():
    """
    Count the number of Wednesdays in ./data/dates.txt and write the count
    to ./data/dates-wednesdays.txt.
    """
    input_path = "./data/dates.txt"
    output_path = "./data/dates-wednesdays.txt"
    if not os.path.isfile(input_path):
        raise Exception(f"File not found: {input_path}")
    count = 0
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                date_obj = parse(line)
                if date_obj.weekday() == 2:  # Wednesday: Monday=0, Tuesday=1, Wednesday=2
                    count += 1
            except Exception:
                continue
    with open(output_path, "w") as f:
        f.write(str(count))
    return f"Counted {count} Wednesdays in dates.txt"


# ---------------------------
# Task A4: Sort contacts.json
# ---------------------------
def task_a4_sort_contacts():
    """
    Sort the array of contacts in ./data/contacts.json by last_name then first_name,
    and write the sorted result to ./data/contacts-sorted.json.
    """
    input_path = "./data/contacts.json"
    output_path = "./data/contacts-sorted.json"
    if not os.path.isfile(input_path):
        raise Exception(f"File not found: {input_path}")
    with open(input_path, "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda c: (
        c.get("last_name", ""), c.get("first_name", "")))
    with open(output_path, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "Sorted contacts and saved to contacts-sorted.json"


# ---------------------------
# Task A5: Extract first line of 10 most recent .log files
# ---------------------------
def task_a5_logs_recent():
    """
    Write the first line of the 10 most recent .log files in ./data/logs/
    to ./data/logs-recent.txt, with the most recent first.
    """
    logs_dir = "./data/logs"
    if not os.path.isdir(logs_dir):
        raise Exception(f"Logs directory not found: {logs_dir}")
    # Get list of .log files with their modification times
    log_files = []
    for file in glob(os.path.join(logs_dir, "*.log")):
        mtime = os.path.getmtime(file)
        log_files.append((mtime, file))
    # Sort by modification time descending (most recent first)
    log_files.sort(key=lambda x: x[0], reverse=True)
    selected_files = log_files[:10]
    lines = []
    for _, filepath in selected_files:
        with open(filepath, "r") as f:
            first_line = f.readline().rstrip("\n")
            lines.append(first_line)
    output_path = "./data/logs-recent.txt"
    with open(output_path, "w") as f:
        for line in lines:
            f.write(line + "\n")
    return "Extracted first lines from 10 most recent .log files to logs-recent.txt"


# ---------------------------
# Task A6: Create docs index
# ---------------------------
def task_a6_create_docs_index():
    """
    Find all Markdown (.md) files in ./data/docs/ (recursively). For each file,
    extract the first occurrence of an H1 (i.e. a line starting with "# "),
    and create an index file ./data/docs/index.json that maps each filename
    (relative to ./data/docs) to its title.
    """
    docs_root = "./data/docs"
    index = {}
    # Walk through docs_root recursively
    for root, dirs, files in os.walk(docs_root):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                # Get relative path (using forward slashes)
                rel_path = os.path.relpath(
                    full_path, docs_root).replace(os.sep, "/")
                title = None
                with open(full_path, "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            break
                if title:
                    index[rel_path] = title
    output_path = os.path.join(docs_root, "index.json")
    with open(output_path, "w") as f:
        json.dump(index, f, indent=2)
    return "Created docs index in docs/index.json"


# ---------------------------
# Task A7: Extract sender's email from email.txt
# ---------------------------
def task_a7_extract_email():
    """
    Read ./data/email.txt, extract the sender's email address,
    and write it to ./data/email-sender.txt.
    """
    input_path = "./data/email.txt"
    output_path = "./data/email-sender.txt"
    if not os.path.isfile(input_path):
        raise Exception(f"File not found: {input_path}")
    with open(input_path, "r") as f:
        content = f.read()
    match = re.search(
        r"From:\s*(?:.*<)?([\w\.-]+@[\w\.-]+\.\w+)(?:>)?", content)
    if not match:
        raise Exception("Could not extract sender email from email.txt")
    sender_email = match.group(1)
    with open(output_path, "w") as f:
        f.write(sender_email)
    return f"Extracted sender email: {sender_email}"


# ---------------------------
# Task A8: Extract credit card number (delegated to LLM service)
# ---------------------------
def extract_credit_card_number():
    BASE_URL = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}"
    }

    image_path = "./data/credit_card.png"
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise Exception("Credit card image not found at the specified path.")

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a test assistant. You are required to extract a credit card number from an image. "
                    "For this test, output exactly and only the credit card number as a sequence of digits, with no spaces, punctuation, or extra text. "
                    "Do not include any apologies, disclaimers, or extra commentary."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the credit card number from the image below. Output only the digits, with no extra text."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        cno = result["choices"][0]["message"]["content"].strip()
        output_path = "./data/credit-card.txt"
        with open(output_path, "w") as f:
            f.write(cno)
        return cno
    else:
        raise Exception(
            f"LLM API error: {response.status_code} {response.text}")


# ---------------------------
# Task A9: Find most similar pair of comments using embeddings
# ---------------------------
def task_a9_find_similar_comments():
    """
    Read ./data/comments.txt (one comment per line), call the embeddings API
    (using model "text-embedding-3-small") to get embeddings for all comments,
    compute pairwise cosine similarities, and write the most similar pair
    (sorted alphabetically, one per line) to ./data/comments-similar.txt.
    """
    input_path = "./data/comments.txt"
    output_path = "./data/comments-similar.txt"
    if not os.path.isfile(input_path):
        raise Exception(f"File not found: {input_path}")
    with open(input_path, "r") as f:
        comments = [line.strip() for line in f if line.strip()]
    if not comments:
        raise Exception("No comments found in comments.txt")

    # Call the embeddings endpoint (synchronously using requests)
    OPENAI_API_BASE = os.getenv(
        "OPENAI_API_BASE", "https://aiproxy.sanand.workers.dev/openai/v1")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {"model": "text-embedding-3-small", "input": comments}
    response = requests.post(
        f"{OPENAI_API_BASE}/embeddings", headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(
            f"Embeddings API error: {response.status_code} {response.text}")
    data = response.json()
    embeddings = np.array([item["embedding"] for item in data["data"]])

    # Compute cosine similarity (using dot product as vectors are normalized)
    similarity = np.dot(embeddings, embeddings.T)
    np.fill_diagonal(similarity, -np.inf)
    i, j = np.unravel_index(similarity.argmax(), similarity.shape)

    selected = sorted([comments[i], comments[j]])
    output_text = "\n".join(selected) + "\n"
    with open(output_path, "w") as f:
        f.write(output_text)
    return "Found most similar comments and wrote to comments-similar.txt"


# ---------------------------
# Task A10: Calculate total sales for Gold tickets
# ---------------------------
def task_a10_total_sales_gold():
    """
    Calculate the total sales for all "Gold" ticket types from the SQLite database
    at ./data/ticket-sales.db and write the result to ./data/ticket-sales-gold.txt.
    Assumes a table `tickets` with columns: type, units, price.
    """
    db_path = "./data/ticket-sales.db"
    output_path = "./data/ticket-sales-gold.txt"
    if not os.path.isfile(db_path):
        raise Exception(f"Database file not found: {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(units * price) FROM tickets WHERE lower(type) = 'gold'")
    result = cur.fetchone()[0]
    if result is None:
        result = 0
    with open(output_path, "w") as f:
        f.write(str(result))
    conn.close()
    return f"Calculated total Gold sales: {result}"
