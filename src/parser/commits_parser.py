import subprocess
import json
from datetime import datetime, timezone

class GitHubCommitFetcher:
    def __init__(self, token_file, repo):
        self.access_token = self._read_token(token_file)
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{repo}/commits"

    def _read_token(self, token_file):
        with open(token_file, 'r') as file:
            return file.read().strip()

    def _construct_curl_command(self):
        return f'''
        curl -L \
          -H "Accept: application/vnd.github+json" \
          -H "Authorization: Bearer {self.access_token}" \
          -H "X-GitHub-Api-Version: 2022-11-28" \
          {self.api_url}
        '''

    def fetch_commits(self):
        try:
            curl_command = self._construct_curl_command()
            result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing curl command: {e.stderr}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
        return None

class CommitParser:
    @staticmethod
    def parse_commit(commit_data):
        sha = commit_data['sha']
        author = commit_data['commit']['author']['name']
        message = commit_data['commit']['message'].split('\n')[0]
        commit_time_str = commit_data['commit']['author']['date']
        commit_time = datetime.strptime(commit_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        formatted_time = commit_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return {
            'sha': sha[:7],
            'author': author,
            'message': message,
            'time': formatted_time
        }