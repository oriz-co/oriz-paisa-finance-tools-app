#!/usr/bin/env python3
"""Deploy to Vercel using the Vercel API."""

import os
import sys
import time
import json
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
VERCEL_ORG_ID = os.getenv("VERCEL_ORG_ID")
VERCEL_PROJECT_ID = os.getenv("VERCEL_PROJECT_ID")
DIST_DIR = Path(__file__).parent.parent / "dist"
TIMEOUT = 300  # 5 minutes


def get_files_for_upload(dist_path: Path) -> list:
    """Get all files formatted for Vercel API."""
    files = []
    for file in dist_path.rglob('*'):
        if file.is_file():
            relative_path = file.relative_to(dist_path)
            with open(file, 'rb') as f:
                content = f.read()
            files.append({
                "file": str(relative_path).replace("\\", "/"),
                "data": base64.b64encode(content).decode('utf-8'),
                "encoding": "base64"
            })
    return files


def deploy_to_vercel() -> bool:
    """Deploy the dist folder to Vercel."""
    if not VERCEL_TOKEN:
        print("❌ VERCEL_TOKEN not set in .env")
        return False

    if not DIST_DIR.exists():
        print(f"❌ Dist folder not found: {DIST_DIR}")
        print("Run 'npm run build' first.")
        return False

    print(f"📦 Preparing files from {DIST_DIR}...")
    files = get_files_for_upload(DIST_DIR)
    print(f"   Found {len(files)} files")

    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "name": "finsuite",
        "files": files,
        "projectSettings": {
            "framework": None
        },
        "target": "production"
    }

    if VERCEL_ORG_ID:
        payload["teamId"] = VERCEL_ORG_ID

    url = "https://api.vercel.com/v13/deployments"

    print("🚀 Deploying to Vercel...")
    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)

        if response.status_code in (200, 201):
            deploy_data = response.json()
            deploy_url = deploy_data.get("url", "")
            elapsed = time.time() - start_time
            print(f"✅ Deployed to Vercel in {elapsed:.1f}s")
            print(f"🔗 URL: https://{deploy_url}")
            return True
        else:
            print(f"❌ Vercel deployment failed: {response.status_code}")
            print(response.text[:500])
            return False

    except requests.exceptions.Timeout:
        print(f"❌ Deployment timed out after {TIMEOUT}s")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


if __name__ == "__main__":
    success = deploy_to_vercel()
    sys.exit(0 if success else 1)
