import os
import sys
from countdown_timer import CountdownTimer
from commits_parser import GitHubCommitFetcher, CommitParser
import time

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def main():
    # Get the path to the access token file
    token_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'access_token'))
    
    repo = 'v8/v8'
    fetcher = GitHubCommitFetcher(token_file, repo)
    timer = CountdownTimer(duration=60)  # 60 seconds countdown
    last_commit_sha = None

    while True:
        print("Fetching latest commit...")
        try:
            commits_data = fetcher.fetch_commits()
            if commits_data:
                latest_commit = commits_data[0]
                parsed_commit = CommitParser.parse_commit(latest_commit)
                if parsed_commit['sha'] != last_commit_sha:
                    print("New commit found")
                    print(f"{parsed_commit['sha']} {parsed_commit['message']}")
                    last_commit_sha = parsed_commit['sha']
                else:
                    print("No update")
            else:
                print("No commits data received.")
        except FileNotFoundError:
            print(f"Error: access_token file not found at {token_file}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        timer.start()
        while timer.get_state() != "finished":
            time.sleep(1)
        
        timer.reset()

if __name__ == "__main__":
    main()