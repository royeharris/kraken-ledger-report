import os
import subprocess
import re

REPO_DIR = "_repo"
VERSIONS_DIR = "_versions"
FILE_NAME = "Kraken Ledger Report.html"

# Ensure absolute paths
base_dir = os.getcwd()
repo_path = os.path.join(base_dir, REPO_DIR)
versions_path = os.path.join(base_dir, VERSIONS_DIR)

os.makedirs(versions_path, exist_ok=True)

# Fetch all entries
print("Fetching tags/branches...")
subprocess.run(["git", "-C", repo_path, "fetch", "--all", "--tags"], check=True)

# Get commits affecting the file
print(f"Analyzing commits for {FILE_NAME}...")
cmd = ["git", "-C", repo_path, "log", "--reverse", "--pretty=format:%h", "--", FILE_NAME]
try:
    commits = subprocess.check_output(cmd, text=True).strip().split('\n')
except subprocess.CalledProcessError as e:
    print(f"Error getting log: {e}")
    commits = []

count = 0
found_248 = False

print(f"Found {len(commits)} commits. Exporting...")

for i, commit in enumerate(commits):
    if not commit: continue
    
    # Get content
    content_cmd = ["git", "-C", repo_path, "show", f"{commit}:{FILE_NAME}"]
    try:
        content = subprocess.check_output(content_cmd)
        content_str = content.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Failed to read commit {commit}: {e}")
        continue

    # Extract version marker (vX.XX)
    # Looking for pattern "v" followed by numbers and dots, typically found in title or span
    # Example: v3.045
    match = re.search(r"v\d+\.\d+", content_str)
    version_tag = ""
    if match:
        version_tag = "_" + match.group(0)
        if "v2.48" in match.group(0):
            found_248 = True
            
    # export filename
    filename = f"{i+1:03d}_{commit}{version_tag}.html"
    dest = os.path.join(versions_path, filename)
    
    with open(dest, "wb") as f:
        f.write(content)
    
    count += 1

print("-" * 30)
print(f"Report:")
print(f"File path used: {os.path.join(repo_path, FILE_NAME)}")
print(f"Number of snapshots exported: {count}")
print(f"Has snapshot with v2.48: {found_248}")
