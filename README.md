# gitscrape
Scrape git* for data

*Input*: one or more GitHub repos

*Output*: Summary data on each GitHub repo in a .csv

# Usage

1. Install dependencies:

```pip install -r requirements.txt```

2. Enter repos to scan into repos.txt

3. Create csv of data with one row per repo.

```python main.py```

# Run tests

```python tests.py```

## Original motivation for gitscrape

Collect basic data on the repos associated with the Julia registry.
