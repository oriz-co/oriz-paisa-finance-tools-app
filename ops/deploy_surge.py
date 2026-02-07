#!/usr/bin/env python3
"""Deploy to Surge.sh using CLI."""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SURGE_TOKEN = os.getenv("SURGE_TOKEN")
SURGE_DOMAIN = os.getenv("SURGE_DOMAIN", "finsuite.surge.sh")
DIST_DIR = Path(__file__).parent.parent / "dist"
TIMEOUT = 300  # 5 minutes


def deploy_to_surge() -> bool:
    """Deploy the dist folder to Surge.sh."""
    if not SURGE_TOKEN:
        print("❌ SURGE_TOKEN not set in .env")
        return False

    if not DIST_DIR.exists():
        print(f"❌ Dist folder not found: {DIST_DIR}")
        print("Run 'npm run build' first.")
        return False

    # Check if surge CLI is installed
    try:
        subprocess.run(["surge", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("❌ Surge CLI not installed. Run: npm install -g surge")
        return False

    print(f"🚀 Deploying to Surge ({SURGE_DOMAIN})...")

    env = os.environ.copy()
    env["SURGE_TOKEN"] = SURGE_TOKEN

    try:
        result = subprocess.run(
            ["surge", str(DIST_DIR), SURGE_DOMAIN],
            env=env,
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )

        if result.returncode == 0:
            print(f"✅ Deployed to Surge!")
            print(f"🔗 URL: https://{SURGE_DOMAIN}")
            return True
        else:
            print(f"❌ Surge deployment failed:")
            print(result.stderr or result.stdout)
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ Deployment timed out after {TIMEOUT}s")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


if __name__ == "__main__":
    success = deploy_to_surge()
    sys.exit(0 if success else 1)
