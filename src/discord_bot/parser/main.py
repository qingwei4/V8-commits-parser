import os
import sys
import argparse
from countdown_timer import CountdownTimer
from commits_parser import GitHubCommitFetcher, CommitParser
import time
from datetime import datetime

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def log_message(message, log_file=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    if log_file:
        with open(log_file, "a") as f:
            f.write(formatted_message + "\n")

def main(log_option):
    # Get the path to the access token file
    token_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'access_token'))
    
    repo = 'v8/v8'
    fetcher = GitHubCommitFetcher(token_file, repo)
    timer = CountdownTimer(duration=60)  # 60 seconds countdown
    last_commit_sha = None
    log_file = "log" if log_option == "log" else None

    while True:
        log_message("Fetching latest commit...", log_file)
        try:
            commits_data = fetcher.fetch_commits()
            if commits_data:
                latest_commit = commits_data[0]
                parsed_commit = CommitParser.parse_commit(latest_commit)
                if parsed_commit['sha'] != last_commit_sha:
                    log_message("New commit found", log_file)
                    log_message(f"{parsed_commit['sha']} {parsed_commit['message']}", log_file)
                    last_commit_sha = parsed_commit['sha']
                else:
                    log_message("No update", log_file)
            else:
                log_message("No commits data received.", log_file)
        except FileNotFoundError:
            log_message(f"Error: access_token file not found at {token_file}", log_file)
        except Exception as e:
            log_message(f"An unexpected error occurred: {e}", log_file)

        timer.start()
        while timer.get_state() != "finished":
            time.sleep(1)
        
        timer.reset()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and log GitHub commits.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--log", action="store_const", const="log", dest="log_option",
                       help="Enable logging to file")
    group.add_argument("--no-log", action="store_const", const="no-log", dest="log_option",
                       help="Disable logging to file")
    args = parser.parse_args()

    if args.log_option is None:
        print("Please specify either --log or --no-log option.")
        print("Use --log to save logs to a file.")
        print("Use --no-log to only print to console.")
        sys.exit(1)

    main(args.log_option)