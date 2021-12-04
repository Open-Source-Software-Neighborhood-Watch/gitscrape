"""GitHub-related functionality."""

import json
import os
import re

import requests

from utils import get_days_since_last_updated

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


def get_github_repo_data(repo):
    """Generate dict of GitHub repo data.

    Args:
        repo (str) : a GitHub repo org and repo name (e.g. "psf/requests")

    Return:
        dict: repo information
    """
    response = requests.get(
        "https://api.github.com/repos/" + repo,
        # convert username and token to strings per requests's specifications
        auth=(str(GITHUB_USERNAME), str(GITHUB_TOKEN)),
    )

    repo_items = json.loads(response.text or response.content)

    repo_dict = {}
    repo_dict["repo_name"] = repo
    repo_dict["forks"] = repo_items["forks"]
    repo_dict["stars"] = repo_items["stargazers_count"]
    repo_dict["num_commits"] = get_number_of_commits(repo)
    repo_dict["num_contributors"] = get_number_of_contributors(repo)
    repo_dict["last_updated"] = get_days_since_last_updated(repo_items["updated_at"])

    return repo_dict


def get_number_of_commits(repo):
    """Retrieve number of commits for a repo.

    Helpful GitHub gist: https://gist.github.com/codsane/25f0fd100b565b3fce03d4bbd7e7bf33#file-commitcount-py

    The trick is to set the 'per_page' parameter value to 1 and then count the
    number of pages.

    Args:
        repo (str) : a GitHub repo org and repo name (e.g. "psf/requests")

    Return:
        int: count of commits
    """
    response = requests.get(
        "https://api.github.com/repos/" + repo + "/commits?per_page=1",
        # convert username and token to strings per requests's specifications
        auth=(str(GITHUB_USERNAME), str(GITHUB_TOKEN)),
    )
    link_field = response.headers["Link"]
    num_contributors = int(re.findall(r"(\d+)>; rel=\"last\"", link_field)[-1])
    return num_contributors


def get_number_of_contributors(repo):
    """Retrieve number of contributors for a repo.

    SO reference used to create this function:
    https://stackoverflow.com/questions/44347339/github-api-how-efficiently-get-the-total-contributors-amount-per-repository

    The trick is to set the 'per_page' parameter value to 1 and then count the
    number of pages.

    Full disclosure: This part of the GitHub API is complicated and hard to figure
    out precisely. The numbers returned from this particular call seem generally
    right, but not precisely right.

    Args:
        repo (str) : a GitHub repo org and repo name (e.g. "psf/requests")

    Return:
        int: count of contributors
    """
    response = requests.get(
        "https://api.github.com/repos/" + repo + "/contributors?per_page=1&anon=true",
        # convert username and token to strings per requests's specifications
        auth=(str(GITHUB_USERNAME), str(GITHUB_TOKEN)),
    )
    link_field = response.headers["Link"]
    # Find number before [>; rel="last"]
    num_contributors = int(re.findall(r"(\d+)>; rel=\"last\"", link_field)[-1])
    return num_contributors


def extract_github_owner_and_repo(github_page):
    """Extract only owner and repo name from GitHub page.

    e.g. https://www.github.com/psf/requests -> psf/requests

    Args:
        github_page - a reference, e.g. a URL, to a GitHub repo
    Returns:
        str: owner and repo joined by a '/'
    """
    if github_page == "":
        return ""

    # split on github.com
    split_github_page = github_page.split("github.com")

    # take portion of URL after github.com and split on slashes
    github_url_elements = split_github_page[1].split("/")

    # rejoin by slash owner and repo name
    github_owner_and_repo = ("/").join(github_url_elements[1:3])

    # strip off new line characters
    github_owner_and_repo = github_owner_and_repo.strip("\n")

    return github_owner_and_repo


def read_in_repo_list(file="repos.txt"):
    """Read in list of repos to analyze.

    Ingests .txt file of repos, creating list of repos
    with each item only containing the repo org and name (e.g. psf/requests)

    Args:
        file (str) - file name containing repos

    Returns:
        list - repos to analyze
    """
    repos = []
    with open(file, "r") as input_repos:
        for repo in input_repos:
            repo_owner_and_name = extract_github_owner_and_repo(repo)
            repos.append(repo_owner_and_name)
    return repos
