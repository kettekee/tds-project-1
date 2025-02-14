import os
import requests
import subprocess


def task_b3_fetch_data(api_url: str, output_filename: str):
    """
    Fetch data from the provided API URL and save the response to ./data/<output_filename>.
    """
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

    output_path = f"./data/{output_filename}"
    with open(output_path, "w") as f:
        f.write(response.text)

    return f"Fetched data from {api_url} and saved to {output_filename}"


def task_b4_clone_repo_and_commit(repo_url: str, commit_message: str):
    """
    Clone a git repository into ./data/repo_temp, create a new file, commit it,
    and (optionally) push the commit. For demonstration purposes, pushing is omitted.
    """
    clone_dir = "./data/repo_temp"
    # Remove the directory if it exists
    import shutil
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

    result = subprocess.run(
        ["git", "clone", repo_url, clone_dir],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception("Failed to clone repository: " + result.stderr)

    # Create a new file to simulate a change
    new_file_path = f"{clone_dir}/new_file.txt"
    with open(new_file_path, "w") as f:
        f.write("Automated commit by LLM-based Automation Agent")

    subprocess.run(["git", "-C", clone_dir, "add", "new_file.txt"], check=True)
    subprocess.run(["git", "-C", clone_dir, "commit",
                   "-m", commit_message], check=True)

    # Pushing the commit would require credentials; this example stops here.
    return f"Cloned repo from {repo_url} and created a commit with message: {commit_message}"


def task_b5_run_sql_query(db_path: str, query: str, output_filename: str):
    """
    Run a SQL query on a SQLite database and write the results to ./data/<output_filename>.
    """
    import sqlite3

    if not os.path.isfile(db_path):
        raise Exception(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    output_path = f"./data/{output_filename}"
    with open(output_path, "w") as f:
        for row in rows:
            f.write(str(row) + "\n")

    return f"Executed SQL query and saved results to {output_filename}"
