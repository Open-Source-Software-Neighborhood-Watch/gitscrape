"""General utilities."""

import csv
import datetime


def get_days_since_last_updated(last_update_date):
    """Calculate number of days from current time to days since last update

    Args:
        last_update_date (str): e.g. 2021-11-06T12:24:34Z

    Returns:
        int - count of days since last update
    """
    last_update_date = datetime.datetime.strptime(
        last_update_date, "%Y-%m-%dT%H:%M:%SZ"
    )
    diff = datetime.datetime.today() - last_update_date

    days_since_last_updated = 0
    if diff.days >= 0:
        days_since_last_updated = diff.days

    return days_since_last_updated


def add_repo_to_csv(repo_dict):
    """Write repo info to existing csv file.

    Use to create dataset of repos for analysis.

    Args:
        repo_dict
    Returns:
        null
    """
    # newline='' prevents spaces in between entries. Setting encoding to utf-8
    # ensures that most (all?) characters can be read. "a" is for append.
    with open("results.csv", "a", encoding="utf-8", newline="") as file:
        fieldnames = ["repo_name", "forks", "stars", "last_updated"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(
            {
                "repo_name": repo_dict["repo_name"],
                "forks": repo_dict["forks"],
                "stars": repo_dict["stars"],
                "last_updated": repo_dict["last_updated"],
            }
        )
