#!/usr/bin/env python3
"""
Deploy to ALL platforms simultaneously.
Orchestrator script that runs all deployment scripts.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

OPS_DIR = Path(__file__).parent
DIST_DIR = OPS_DIR.parent / "dist"

DEPLOYMENTS = {
    "cloudflare": {
        "script": None,  # Uses wrangler CLI
        "enabled": os.getenv("ENABLE_CLOUDFLARE", "True").lower() == "true",
        "url": "https://money.chirag127.in",
    },
    "netlify": {
        "script": OPS_DIR / "deploy_netlify.py",
        "enabled": os.getenv("ENABLE_NETLIFY", "True").lower() == "true",
        "url": "https://finsuite.netlify.app",
    },
    "vercel": {
        "script": OPS_DIR / "deploy_vercel.py",
        "enabled": os.getenv("ENABLE_VERCEL", "True").lower() == "true",
        "url": "https://finsuite.vercel.app",
    },
    "surge": {
        "script": OPS_DIR / "deploy_surge.py",
        "enabled": os.getenv("ENABLE_SURGE", "True").lower() == "true",
        "url": "https://finsuite.surge.sh",
    },
    "neocities": {
        "script": OPS_DIR / "deploy_neocities.py",
        "enabled": os.getenv("ENABLE_NEOCITIES", "True").lower() == "true",
        "url": "https://chirag127.neocities.org",
    },
    "github_pages": {
        "script": OPS_DIR / "deploy_github_pages.py",
        "enabled": True,
        "url": "https://chirag127.github.io/finsuite",
    },
}


def build_project() -> bool:
    """Build the project using npm."""
    print("🔨 Building project...")
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=OPS_DIR.parent,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("✅ Build successful")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def deploy_cloudflare() -> tuple:
    """Deploy to Cloudflare Pages using wrangler."""
    start = time.time()
    try:
        result = subprocess.run(
            ["npx", "wrangler", "pages", "deploy", str(DIST_DIR), "--project-name=finsuite"],
            cwd=OPS_DIR.parent,
            capture_output=True,
            text=True,
            timeout=300
        )
        elapsed = time.time() - start
        if result.returncode == 0:
            return ("cloudflare", True, elapsed, "https://money.chirag127.in")
        else:
            return ("cloudflare", False, elapsed, result.stderr[:200])
    except Exception as e:
        return ("cloudflare", False, time.time() - start, str(e))


def deploy_platform(name: str, config: dict) -> tuple:
    """Deploy to a specific platform."""
    if not config["enabled"]:
        return (name, None, 0, "Disabled")

    if name == "cloudflare":
        return deploy_cloudflare()

    script = config["script"]
    if not script or not script.exists():
        return (name, False, 0, "Script not found")

    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=300
        )
        elapsed = time.time() - start
        success = result.returncode == 0
        message = config["url"] if success else result.stderr[:200]
        return (name, success, elapsed, message)
    except subprocess.TimeoutExpired:
        return (name, False, 300, "Timeout")
    except Exception as e:
        return (name, False, time.time() - start, str(e))


def deploy_all(parallel: bool = True) -> dict:
    """Deploy to all enabled platforms."""
    results = {}

    if parallel:
        print("🚀 Deploying to all platforms in parallel...\n")
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                executor.submit(deploy_platform, name, config): name
                for name, config in DEPLOYMENTS.items()
            }

            for future in as_completed(futures):
                name, success, elapsed, message = future.result()
                results[name] = {"success": success, "time": elapsed, "message": message}

                if success is None:
                    print(f"⏭️  {name}: Skipped (disabled)")
                elif success:
                    print(f"✅ {name}: Deployed in {elapsed:.1f}s → {message}")
                else:
                    print(f"❌ {name}: Failed ({message})")
    else:
        print("🚀 Deploying to all platforms sequentially...\n")
        for name, config in DEPLOYMENTS.items():
            name, success, elapsed, message = deploy_platform(name, config)
            results[name] = {"success": success, "time": elapsed, "message": message}

            if success is None:
                print(f"⏭️  {name}: Skipped (disabled)")
            elif success:
                print(f"✅ {name}: Deployed in {elapsed:.1f}s → {message}")
            else:
                print(f"❌ {name}: Failed ({message})")

    return results


def print_summary(results: dict):
    """Print deployment summary."""
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 60)

    successful = []
    failed = []
    skipped = []

    for name, result in results.items():
        if result["success"] is None:
            skipped.append(name)
        elif result["success"]:
            successful.append(name)
        else:
            failed.append(name)

    print(f"\n✅ Successful: {len(successful)}")
    for name in successful:
        url = DEPLOYMENTS[name]["url"]
        print(f"   • {name}: {url}")

    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for name in failed:
            print(f"   • {name}: {results[name]['message']}")

    if skipped:
        print(f"\n⏭️  Skipped: {len(skipped)}")
        for name in skipped:
            print(f"   • {name}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Parse arguments
    skip_build = "--skip-build" in sys.argv
    sequential = "--sequential" in sys.argv

    if not skip_build:
        if not build_project():
            print("\n❌ Build failed. Aborting deployment.")
            sys.exit(1)
        print()

    results = deploy_all(parallel=not sequential)
    print_summary(results)

    # Exit code based on results
    successful = sum(1 for r in results.values() if r["success"] is True)
    sys.exit(0 if successful > 0 else 1)
