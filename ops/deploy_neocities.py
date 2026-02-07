#!/usr/bin/env python3
"""Deploy to Neocities using their API."""

import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

NEOCITIES_API_KEY = os.getenv("NEOCITIES_API_KEY")
NEOCITIES_SITENAME = os.getenv("NEOCITIES_SITENAME", "chirag127")
DIST_DIR = Path(__file__).parent.parent / "dist"
TIMEOUT = 300  # 5 minutes

# File extensions that Neocities allows
ALLOWED_EXTENSIONS = {
    '.html', '.htm', '.css', '.js', '.json', '.txt', '.md', '.xml',
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp',
    '.woff', '.woff2', '.ttf', '.eot', '.otf',
    '.mp3', '.mp4', '.ogg', '.wav', '.webm',
    '.pdf', '.zip', '.csv'
}


def is_allowed_file(filepath: Path) -> bool:
    """Check if file extension is allowed by Neocities."""
    return filepath.suffix.lower() in ALLOWED_EXTENSIONS


def deploy_to_neocities() -> bool:
    """Deploy the dist folder to Neocities."""
    if not NEOCITIES_API_KEY:
        print("❌ NEOCITIES_API_KEY not set in .env")
        return False

    if not DIST_DIR.exists():
        print(f"❌ Dist folder not found: {DIST_DIR}")
        print("Run 'npm run build' first.")
        return False

    headers = {
        "Authorization": f"Bearer {NEOCITIES_API_KEY}",
    }

    print(f"📦 Preparing files from {DIST_DIR}...")
    files_to_upload = []
    skipped = 0

    for file in DIST_DIR.rglob('*'):
        if file.is_file():
            if is_allowed_file(file):
                relative_path = str(file.relative_to(DIST_DIR)).replace("\\", "/")
                files_to_upload.append((file, relative_path))
            else:
                skipped += 1

    print(f"   Found {len(files_to_upload)} files (skipped {skipped} unsupported)")

    print(f"🚀 Deploying to Neocities ({NEOCITIES_SITENAME})...")
    start_time = time.time()

    # Upload in batches of 10 files
    batch_size = 10
    uploaded = 0
    failed = 0

    for i in range(0, len(files_to_upload), batch_size):
        batch = files_to_upload[i:i + batch_size]
        files = {}

        for filepath, relative_path in batch:
            with open(filepath, 'rb') as f:
                files[relative_path] = (relative_path, f.read())

        try:
            response = requests.post(
                "https://neocities.org/api/upload",
                headers=headers,
                files=files,
                timeout=TIMEOUT
            )

            if response.status_code == 200:
                uploaded += len(batch)
                print(f"   Uploaded {uploaded}/{len(files_to_upload)} files...")
            else:
                failed += len(batch)
                print(f"   ⚠️ Batch failed: {response.text[:100]}")

        except Exception as e:
            failed += len(batch)
            print(f"   ⚠️ Batch error: {e}")

    elapsed = time.time() - start_time

    if failed == 0:
        print(f"✅ Deployed to Neocities in {elapsed:.1f}s")
        print(f"🔗 URL: https://{NEOCITIES_SITENAME}.neocities.org")
        return True
    elif uploaded > 0:
        print(f"⚠️ Partial deployment: {uploaded} succeeded, {failed} failed")
        return True
    else:
        print(f"❌ Deployment failed")
        return False


if __name__ == "__main__":
    success = deploy_to_neocities()
    sys.exit(0 if success else 1)
