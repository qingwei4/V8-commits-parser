from commits_parser import GitHubCommitFetcher, CommitParser

def main():
    # Initialize the GitHubCommitFetcher
    token_file = 'access_token'
    repo = 'v8/v8'
    fetcher = GitHubCommitFetcher(token_file, repo)

    try:
        # Fetch commits
        commits = fetcher.fetch_commits()

        if commits:
            print(f"Successfully fetched commits from {repo}")
            print("Recent commits:")
            for commit in commits:  # Now processing all commits
                try:
                    parsed_commit = CommitParser.parse_commit(commit)
                    print(f"Commit: {parsed_commit['sha']} | Author: {parsed_commit['author']} | Message: {parsed_commit['message']}")
                    print("---")
                except KeyError as e:
                    print(f"Error parsing commit: {e}")
                except Exception as e:
                    print(f"Unexpected error parsing commit: {e}")
        else:
            print("No commits received.")

    except FileNotFoundError:
        print("Error: access_token file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()