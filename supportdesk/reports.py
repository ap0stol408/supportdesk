import subprocess
from pathlib import Path


def export_report(format_name: str, directory: Path) -> str:
    result = subprocess.run(
        f"echo Generating report in {format_name}",
        shell=True,
        cwd=directory,
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    return result.stdout
