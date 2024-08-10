import subprocess
import json
from datetime import datetime, timezone

# Read the access token from the file
with open('access_token', 'r') as token_file:
    access_token = token_file.read().strip()

# Construct the curl command
curl_command = f'''
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer {access_token}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/v8/v8/commits
'''

# Execute the curl command and capture the output
try:
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, check=True)
    
    # Parse the JSON response
    commits_data = json.loads(result.stdout)
    
    # Process the commits data as needed
    for commit in commits_data:
        sha = commit['sha']
        author = commit['commit']['author']['name']
        message = commit['commit']['message'].split('\n')[0]  # Get the first line of the commit message
        
        # Parse the commit time
        commit_time_str = commit['commit']['author']['date']
        commit_time = datetime.strptime(commit_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        # Format the time as a string (adjust the format as needed)
        formatted_time = commit_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        print(f"Commit: {sha[:7]} | Author: {author} | Message: {message}")

except subprocess.CalledProcessError as e:
    print(f"Error executing curl command: {e.stderr}")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON response: {e}")
except KeyError as e:
    print(f"Error accessing commit data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")