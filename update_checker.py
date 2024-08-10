from commits_parser import GitHubCommitFetcher, CommitParser

class UpdateChecker:
    def __init__(self, token_file, repo):
        self.fetcher = GitHubCommitFetcher(token_file, repo)
        self.latest_commit_sha = None

    def check_for_updates(self):
        try:
            commits = self.fetcher.fetch_commits()
            if commits:
                newest_commit = CommitParser.parse_commit(commits[0])
                if self.latest_commit_sha != newest_commit['sha']:
                    self.latest_commit_sha = newest_commit['sha']
                    return True, commits
            return False, None
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False, None

    def print_commits(self, commits):
        if commits:
            print("Recent commits:")
            for commit in commits:
                try:
                    parsed_commit = CommitParser.parse_commit(commit)
                    print(f"Commit: {parsed_commit['sha']} | Author: {parsed_commit['author']} | Message: {parsed_commit['message']}")
                    print("---")
                except KeyError as e:
                    print(f"Error parsing commit: {e}")
                except Exception as e:
                    print(f"Unexpected error parsing commit: {e}")
        else:
            print("No commits to display.")
