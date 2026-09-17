import os
import subprocess
from pathlib import Path

def run_script(script_name):
    print(f"=========================================")
    print(f"Running {script_name}...")
    print(f"=========================================")
    result = subprocess.run(["python", f"src/{script_name}"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)
        
def main():
    scripts = [
        # "profiling.py",
        "cleaning.py",
        "feature_engineering.py",
        "sql_loader.py",
        "eda.py"
    ]
    
    for s in scripts:
        run_script(s)

if __name__ == "__main__":
    main()
