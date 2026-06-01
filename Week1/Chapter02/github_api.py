"""GitHub API utilities for fetching repository information."""

import json
import logging
import os
import urllib.request
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")


@dataclass
class RepoInfo:
    """Structured repository information fetched from GitHub API."""

    full_name: str
    description: Optional[str]
    stars: int
    forks: int
    source_url: str
    language: Optional[str]
    topics: list[str]


def get_repo_info(repo: str, token: Optional[str] = None) -> RepoInfo:
    """Fetch repository metadata from the GitHub API.

    Args:
        repo: Repository identifier in "owner/repo" format (e.g. "anomalyco/opencode").
        token: Optional GitHub personal access token for higher rate limits.

    Returns:
        RepoInfo dataclass containing stars, forks, description, and related metadata.

    Raises:
        ValueError: If the repo argument is not in "owner/repo" format.
        urllib.error.HTTPError: On HTTP errors (e.g. 404 Not Found, 403 rate limit).
        urllib.error.URLError: On network/connection failures.
    """
    if "/" not in repo or repo.count("/") != 1:
        raise ValueError(
            f"Invalid repo format: '{repo}'. Expected 'owner/repo'."
        )

    url = f"{GITHUB_API_BASE}/repos/{repo}"
    logger.info("Fetching repo info for %s from %s", repo, url)

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    repo_info = RepoInfo(
        full_name=data.get("full_name", repo),
        description=data.get("description"),
        stars=data.get("stargazers_count", 0),
        forks=data.get("forks_count", 0),
        source_url=data.get("html_url", ""),
        language=data.get("language"),
        topics=data.get("topics", []),
    )

    logger.info(
        "Repo %s: %d stars, %d forks",
        repo_info.full_name,
        repo_info.stars,
        repo_info.forks,
    )
    return repo_info
