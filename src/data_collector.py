"""Data collection from LinkedIn, Twitter/X, and GitHub."""

import requests
import json


def fetch_github(url: str) -> dict:
    """Fetch GitHub profile and repos via public API."""
    # Extract username from URL
    username = url.rstrip("/").split("/")[-1]
    if username.startswith("@"):
        username = username[1:]

    base = "https://api.github.com"
    headers = {"Accept": "application/vnd.github.v3+json"}

    # Fetch profile
    profile_resp = requests.get(f"{base}/users/{username}", headers=headers, timeout=15)
    profile = profile_resp.json() if profile_resp.ok else {}

    # Fetch repos
    repos_resp = requests.get(
        f"{base}/users/{username}/repos?sort=updated&per_page=15",
        headers=headers, timeout=15
    )
    repos = repos_resp.json() if repos_resp.ok else []

    # Fetch starred repos (shows taste)
    starred_resp = requests.get(
        f"{base}/users/{username}/starred?per_page=30",
        headers=headers, timeout=15
    )
    starred = starred_resp.json() if starred_resp.ok else []

    # Format output
    result = {
        "username": profile.get("login", username),
        "name": profile.get("name", ""),
        "bio": profile.get("bio", ""),
        "company": profile.get("company", ""),
        "location": profile.get("location", ""),
        "blog": profile.get("blog", ""),
        "public_repos": profile.get("public_repos", 0),
        "followers": profile.get("followers", 0),
        "following": profile.get("following", 0),
        "created_at": profile.get("created_at", ""),
        "hireable": profile.get("hireable"),
        "repos": [],
        "starred": [],
    }

    for repo in repos:
        if isinstance(repo, dict):
            result["repos"].append({
                "name": repo.get("name", ""),
                "description": repo.get("description", ""),
                "language": repo.get("language", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "updated_at": repo.get("updated_at", ""),
            })

    for star in starred:
        if isinstance(star, dict):
            result["starred"].append({
                "name": star.get("full_name", ""),
                "description": star.get("description", ""),
                "stars": star.get("stargazers_count", 0),
            })

    return result


def fetch_via_jina(url: str) -> str:
    """Fetch any URL content via Jina Reader API."""
    jina_url = f"https://r.jina.ai/{url}"
    headers = {"Accept": "text/markdown"}
    try:
        resp = requests.get(jina_url, headers=headers, timeout=30)
        if resp.ok and len(resp.text) > 100:
            return resp.text
    except Exception:
        pass
    return ""


def fetch_twitter(url: str) -> str:
    """Fetch Twitter/X profile via Jina Reader."""
    content = fetch_via_jina(url)
    if content:
        return content
    return ""


def fetch_linkedin(url: str) -> str:
    """Fetch LinkedIn profile via Jina Reader. Falls back to manual input."""
    content = fetch_via_jina(url)
    if content:
        return content
    return ""


def format_github_for_eval(data: dict) -> str:
    """Format GitHub data as readable text for agent evaluation."""
    lines = []
    lines.append(f"=== GITHUB PROFILE ===")
    lines.append(f"Username: {data['username']}")
    if data["name"]:
        lines.append(f"Name: {data['name']}")
    if data["bio"]:
        lines.append(f"Bio: {data['bio']}")
    if data["company"]:
        lines.append(f"Company: {data['company']}")
    if data["location"]:
        lines.append(f"Location: {data['location']}")
    if data["blog"]:
        lines.append(f"Website: {data['blog']}")
    lines.append(f"Public Repos: {data['public_repos']}")
    lines.append(f"Followers: {data['followers']}")
    lines.append(f"Following: {data['following']}")
    lines.append(f"Account Created: {data['created_at']}")

    if data["repos"]:
        lines.append(f"\n--- Repositories (most recent) ---")
        for repo in data["repos"]:
            desc = f" — {repo['description']}" if repo["description"] else ""
            lang = f" [{repo['language']}]" if repo["language"] else ""
            stars = f" ({repo['stars']}★)" if repo["stars"] else ""
            lines.append(f"  • {repo['name']}{lang}{stars}{desc}")

    if data["starred"]:
        lines.append(f"\n--- Starred Repos (showing taste/interests) ---")
        for star in data["starred"][:20]:
            desc = f" — {star['description'][:80]}" if star.get("description") else ""
            lines.append(f"  • {star['name']} ({star.get('stars', 0)}★){desc}")

    return "\n".join(lines)


def collect_all(linkedin_url: str, twitter_url: str, github_url: str) -> dict:
    """Collect all candidate data. Returns dict with raw and formatted data."""
    github_data = fetch_github(github_url)
    twitter_data = fetch_twitter(twitter_url)
    linkedin_data = fetch_linkedin(linkedin_url)

    # Build combined text for agents
    sections = []

    if linkedin_data:
        sections.append(f"=== LINKEDIN PROFILE ===\n{linkedin_data}")
    else:
        sections.append("=== LINKEDIN PROFILE ===\n[Data unavailable — LinkedIn blocked automated access]")

    if twitter_data:
        sections.append(f"=== TWITTER/X PROFILE ===\n{twitter_data}")
    else:
        sections.append("=== TWITTER/X PROFILE ===\n[Data unavailable]")

    sections.append(format_github_for_eval(github_data))

    return {
        "github": github_data,
        "twitter_raw": twitter_data,
        "linkedin_raw": linkedin_data,
        "combined_text": "\n\n".join(sections),
        "candidate_name": github_data.get("name") or github_data.get("username", "Unknown"),
    }
