"""Tests for gitscrape."""

import unittest

from github import (
    extract_github_owner_and_repo,
    get_github_repo_data,
    get_number_of_contributors,
    read_in_repo_list,
)
from utils import get_days_since_last_updated


class TestGitHubFunctions(unittest.TestCase):
    """Test GitHub-related functions."""

    def test_get_github_repo_data(self):
        """Check get_github_repo_data()."""
        test_data = get_github_repo_data("psf/requests")
        self.assertTrue(isinstance(test_data, dict))
        self.assertTrue(test_data["repo_name"] == "psf/requests")
        self.assertTrue(test_data["stars"] > 1000)
        self.assertTrue(test_data["forks"] > 1000)
        self.assertTrue(test_data["last_updated"] < 1000)
        self.assertTrue(test_data["num_contributors"] > 700)

    def test_extract_github_owner_and_repo(self):
        """Check extract_github_owner_and_repo()."""
        test_owner_and_repo = extract_github_owner_and_repo(
            "www.github.com/psf/requests"
        )
        self.assertTrue(test_owner_and_repo == "psf/requests")
        test_owner_and_repo = extract_github_owner_and_repo(
            "www.github.com/iqtlabs/networkml"
        )
        self.assertTrue(test_owner_and_repo == "iqtlabs/networkml")

    def test_read_in_repo_list(self):
        """Check read_in_repo_list()."""
        test_repo_list = read_in_repo_list("test/test_repos.txt")
        self.assertTrue(test_repo_list == ["psf/requests", "iqtlabs/networkml"])

    def test_get_number_of_contributors(self):
        """Check get_number_of_contributors()."""
        test_num_contributors = get_number_of_contributors("iqtlabs/networkml")
        self.assertTrue(test_num_contributors >= 24)
        self.assertTrue(test_num_contributors <= 100)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def test_get_days_since_last_updated(self):
        """Check days_since_last_updated()."""
        test_days = get_days_since_last_updated("2021-10-06T12:24:34Z")
        self.assertTrue(test_days > 28)
        # any negative values should be reset to 0
        test_days = get_days_since_last_updated("2031-10-06T12:24:34Z")
        self.assertTrue(test_days == 0)


if __name__ == "__main__":
    unittest.main()
