import subprocess
import requests
import sys
import os
import logging

logging.basicConfig(filename='git_poll.log', level=logging.INFO, format='%(asctime)s %(message)s')

def run_cmd(cmd, cwd=None):
    result = subprocess.run(
            cmd,
            shell = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            cwd = cwd
            text=True
    )
    
    if result.returncode != 0:
        raise Exception (f"Execution error {cmd}: {result.stderr.strip()}")
    return result.stdout.strip()

def get_latest_commit(repo_path):
    return run_cmd("git rev-parse origin/main", cwd=repo_path)

def update_repo(repo_url, repo_path):
    if not os.path.isdir(repo_path):
        logging.info("Cloning repository...")
        run_cmd(f"git clone {repo_url} {repo_path}")
    else:
        logging.info("Updating repository...")
        run_cmd("git fetch origin", cwd=repo_path)
        run_cmd("git reset --hard origin/main", cwd=repo_path)

def main(repo_url, last_commit_hash, backend_url):
    repo_path = "./repo_temp"

    try:
        update_repo(repo_url, repo_path)
        latest_commit = get_latest_commit(repo_path)

        logging.info(f"Last commit in repo: {latest_commit}")
        logging.info(f"Last commit processed: {last_commit_hash}")
        
        if latest_commit != last_commit_hash:
            logging.info("New commit detected, launching pipeline...")
            response = requests.post(backend_url, json={"commit": latest_commit})

            if response.status_code == 200:
                logging.info(f"Pipeline successfully launched for commit! {latest_commit}")
                print(latest_commit)
            else:
                logging.error(f"Error launching pipeline: {response.status_code} {response.text}")

        else:
            logging.info("No new commits")

    except Exception as e:
        logging.error(f"Execution error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Use: python3 git_poll.py <repo_url> <last_commit_hash> <backend_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    last_commit_hash = sys.argv[2]
    backend_url = sys.argv[3]

    main(repo_url, last_commit_hash, backend_url)
