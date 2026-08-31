#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    gradle_results_dir = project_dir / "build" / "test-results" / "test"
    ci_results_dir = project_dir / "test-results"

    # Remove reports from prior runs so CI can never publish stale results.
    shutil.rmtree(gradle_results_dir, ignore_errors=True)
    shutil.rmtree(ci_results_dir, ignore_errors=True)
    ci_results_dir.mkdir(parents=True)

    if os.name == "nt":
        wrapper = project_dir / "gradlew.bat"
        command = ["cmd.exe", "/d", "/c", str(wrapper), "cleanTest", "test"]
    else:
        wrapper = project_dir / "gradlew"
        command = [str(wrapper), "cleanTest", "test"]

    if not wrapper.is_file():
        print(f"Gradle wrapper not found: {wrapper}", file=sys.stderr)
        return 1

    try:
        gradle_exit_code = subprocess.run(
            command,
            cwd=project_dir,
            check=False,
        ).returncode
    except OSError as error:
        print(f"Unable to run the Gradle wrapper: {error}", file=sys.stderr)
        return 1

    reports = sorted(gradle_results_dir.glob("*.xml"))
    for report in reports:
        shutil.copy2(report, ci_results_dir / report.name)

    if not reports:
        print(
            f"No JUnit XML reports were generated in {gradle_results_dir}.",
            file=sys.stderr,
        )
        return gradle_exit_code or 1

    print(f"Copied {len(reports)} JUnit XML report(s) to {ci_results_dir}.")
    return gradle_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
