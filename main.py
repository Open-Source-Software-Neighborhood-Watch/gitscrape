"""Scrape github for data from repositories."""

from github import get_github_repo_data, read_in_repo_list
from utils import add_repo_to_csv

if __name__ == "__main__":
    repos = read_in_repo_list()
    for repo in repos:
        try:
            data = get_github_repo_data(repo)
            add_repo_to_csv(data)
        except:
            pass
