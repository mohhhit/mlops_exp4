import argparse
import subprocess
import sys

def run_command(command):
    print(f"\n{'='*60}")
    print(f"RUNNING: {command}")
    print(f"{'='*60}")
    result = subprocess.run([sys.executable] + command.split()[1:], capture_output=False)
    if result.returncode != 0:
        print(f"ERROR: Command failed with code {result.returncode}: {command}")
        sys.exit(result.returncode)

def run_pipeline(version="v1"):
    print(f"\n{'#'*60}")
    print(f"  STARTING MLOPS DATA PIPELINE (VERSION: {version.upper()})")
    print(f"{'#'*60}")
    
    run_command(f"python ingestion.py --version {version}")
    run_command(f"python preprocessing.py --version {version}")
    run_command(f"python transformation.py --version {version}")
    run_command(f"python validation.py --version {version}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Air Quality MLOps End-to-End Pipeline")
    parser.add_argument("--version", type=str, default="v1", choices=["v1", "v2", "all"],
                        help="Pipeline version to execute ('v1', 'v2', or 'all')")
    args = parser.parse_args()

    if args.version == "all":
        run_pipeline("v1")
        run_pipeline("v2")
    else:
        run_pipeline(args.version)

    print("\n" + "#"*60)
    print("  ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")
    print("#"*60)

