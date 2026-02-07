#!/usr/bin/env python3
"""Deploy to GitHub Pages using gh-pages branch."""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GH_USERNAME = os.getenv("GH_USERNAME", "chirag127")
GH_TOKEN = os.getenv("GH_TOKEN")
DIST_DIR = Path(__file__).parent.parent / "dist"
REPO_NAME = "finsuite"
TIMEOUT = 300  # 5 minutes


def deploy_to_github_pages() -> bool:
    """Deploy the dist folder to GitHub Pages."""
    if not GH_TOKEN:
        print("❌ GH_TOKEN not set in .env")
        return False

    if not DIST_DIR.exists():
        print(f"❌ Dist folder not found: {DIST_DIR}")
        print("Run 'npm run build' first.")
        return False

    # Create a temporary directory for gh-pages
    gh_pages_dir = DIST_DIR.parent / ".gh-pages-deploy"
    if gh_pages_dir.exists():
        shutil.rmtree(gh_pages_dir)
    gh_pages_dir.mkdir()

    try:
        print("📦 Preparing GitHub Pages deployment...")

        # Copy dist contents
        for item in DIST_DIR.iterdir():
            dest = gh_pages_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # Create .nojekyll file (for SPA routing)
        (gh_pages_dir / ".nojekyll").touch()

        # Initialize git repo
        os.chdir(gh_pages_dir)

        commands = [
            ["git", "init"],
            ["git", "config", "user.name", GH_USERNAME],
            ["git", "config", "user.email", f"{GH_USERNAME}@users.noreply.github.com"],
            ["git", "add", "-A"],
            ["git", "commit", "-m", "Deploy to GitHub Pages"],
            ["git", "branch", "-M", "gh-pages"],
        ]

        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                print(f"   {' '.join(cmd)}: {result.stderr or result.stdout}")

        # Push to GitHub
        remote_url = f"https://{GH_USERNAME}:{GH_TOKEN}@github.com/{GH_USERNAME}/{REPO_NAME}.git"

        print(f"🚀 Pushing to GitHub Pages...")
        result = subprocess.run(
            ["git", "push", "-f", remote_url, "gh-pages"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )

        if result.returncode == 0:
            print(f"✅ Deployed to GitHub Pages!")
            print(f"🔗 URL: https://{GH_USERNAME}.github.io/{REPO_NAME}")
            return True
        else:
            print(f"❌ GitHub Pages deployment failed:")
            # Don't print the URL with token
            error = result.stderr.replace(GH_TOKEN, "***")
            print(error)
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ Deployment timed out after {TIMEOUT}s")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False
    finally:
        os.chdir(DIST_DIR.parent)
        if gh_pages_dir.exists():
            shutil.rmtree(gh_pages_dir)


if __name__ == "__main__":
    success = deploy_to_github_pages()
    sys.exit(0 if success else 1)
