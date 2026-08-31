#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    results_dir = project_dir / "test-results"
    report_file = results_dir / "junit.xml"

    npm = shutil.which("npm")
    if npm is None:
        print("Error: npm is required but was not found in PATH.", file=sys.stderr)
        return 127

    results_dir.mkdir(parents=True, exist_ok=True)
    report_file.unlink(missing_ok=True)

    try:
        completed = subprocess.run(
            [npm, "test"],
            cwd=project_dir,
            check=False,
        )
    except OSError as error:
        print(f"Error: could not run npm: {error}", file=sys.stderr)
        return 1

    if completed.returncode != 0:
        return completed.returncode

    if not report_file.is_file() or report_file.stat().st_size == 0:
        print(
            f"Error: Karma did not generate {report_file}.",
            file=sys.stderr,
        )
        return 1

    print(f"JUnit test report generated at {report_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
