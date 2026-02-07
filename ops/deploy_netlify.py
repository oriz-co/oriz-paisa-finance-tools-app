#!/usr/bin/env python3
"""Deploy to Netlify using the Netlify API."""

import os
import sys
import time
import zipfile
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

NETLIFY_AUTH_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")
NETLIFY_SITE_ID = os.getenv("NETLIFY_SITE_ID")
DIST_DIR = Path(__file__).parent.parent / "dist"
TIMEOUT = 300  # 5 minutes


def create_zip_archive(dist_path: Path) -> Path:
    """Create a zip archive of the dist folder."""
    zip_path = dist_path.parent / "dist.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in dist_path.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(dist_path)
                zipf.write(file, arcname)
    return zip_path


def deploy_to_netlify() -> bool:
    """Deploy the dist folder to Netlify."""
    if not NETLIFY_AUTH_TOKEN:
        print("❌ NETLIFY_AUTH_TOKEN not set in .env")
        return False

    if not NETLIFY_SITE_ID:
        print("❌ NETLIFY_SITE_ID not set in .env")
        return False

    if not DIST_DIR.exists():
        print(f"❌ Dist folder not found: {DIST_DIR}")
        print("Run 'npm run build' first.")
        return False

    print(f"📦 Creating zip archive of {DIST_DIR}...")
    zip_path = create_zip_archive(DIST_DIR)

    headers = {
        "Authorization": f"Bearer {NETLIFY_AUTH_TOKEN}",
        "Content-Type": "application/zip",
    }

    url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys"

    print(f"🚀 Deploying to Netlify (site: {NETLIFY_SITE_ID})...")
    start_time = time.time()

    try:
        with open(zip_path, 'rb') as f:
            response = requests.post(url, headers=headers, data=f, timeout=TIMEOUT)

        if response.status_code in (200, 201):
            deploy_data = response.json()
            deploy_url = deploy_data.get("deploy_ssl_url", deploy_data.get("url", ""))
            elapsed = time.time() - start_time
            print(f"✅ Deployed to Netlify in {elapsed:.1f}s")
            print(f"🔗 URL: {deploy_url}")
            return True
        else:
            print(f"❌ Netlify deployment failed: {response.status_code}")
            print(response.text)
            return False

    except requests.exceptions.Timeout:
        print(f"❌ Deployment timed out after {TIMEOUT}s")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False
    finally:
        if zip_path.exists():
            zip_path.unlink()


if __name__ == "__main__":
    success = deploy_to_netlify()
    sys.exit(0 if success else 1)
