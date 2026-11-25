"""Check that the Docker image tags in variables.yml exist on Docker Hub.

The quickstart pages build their `docker run` commands from `tag` and
`arm_tag`. A tag that was never published (for example a version number
that skipped a build suffix) breaks the first command a new user runs.

Usage: check_image_tags.py [variables.yml]

Exit 1 if a tag is confirmed missing (HTTP 404). A Docker Hub outage or
rate limit only prints a warning, so it does not block documentation PRs.
"""
import re
import sys
import urllib.error
import urllib.request

API = "https://hub.docker.com/v2/repositories/percona/percona-server/tags/{}"
KEYS = ("tag", "arm_tag")


def read_tags(path):
    text = open(path, encoding="utf-8").read()
    tags = {}
    for key in KEYS:
        match = re.search(rf"^{key}:\s*['\"]?([^'\"\s#]+)", text, re.MULTILINE)
        if not match:
            sys.exit(f"{path}: no '{key}' entry found")
        tags[key] = match.group(1)
    return tags


def tag_exists(tag):
    """Return True/False, or None if Docker Hub could not give an answer."""
    try:
        with urllib.request.urlopen(API.format(tag), timeout=20):
            return True
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return False
        print(f"warning: Docker Hub returned HTTP {err.code} for {tag}; skipping")
    except (urllib.error.URLError, TimeoutError) as err:
        print(f"warning: could not reach Docker Hub for {tag} ({err}); skipping")
    return None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "variables.yml"
    missing = []
    for key, tag in read_tags(path).items():
        if tag_exists(tag) is False:
            missing.append(f"{key}: {tag}")
        else:
            print(f"ok: {key} {tag}")
    if missing:
        print("Tags not found on Docker Hub (percona/percona-server):")
        print("\n".join(f"  {m}" for m in missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
