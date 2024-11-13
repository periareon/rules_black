"""A script for applying black fixes to Bazel targets."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Sequence

import black
from python.runfiles import Runfiles


def _rlocation(runfiles: Runfiles, rlocationpath: str) -> Path:
    """Look up a runfile and ensure the file exists

    Args:
        runfiles: The runfiles object
        rlocationpath: The runfile key

    Returns:
        The requested runifle.
    """
    runfile = runfiles.Rlocation(
        rlocationpath, source_repo=os.getenv("REPOSITORY_NAME")
    )
    if not runfile:
        raise FileNotFoundError(f"Failed to find runfile: {rlocationpath}")
    path = Path(runfile)
    if not path.exists():
        raise FileNotFoundError(f"Runfile does not exist: ({rlocationpath}) {path}")
    return path


def find_bazel() -> Path:
    """Determine the path to a Bazel binary.

    Returns:
        The path to a Bazel binary.
    """
    if "BAZEL_REAL" in os.environ:
        return Path(os.environ["BAZEL_REAL"])

    for path in ["bazel", "bazel.exe", "bazelisk", "bazelisk.exe"]:
        path_bazel = shutil.which(path)
        if path_bazel:
            return Path(path_bazel)

    raise FileNotFoundError("Could not locate a Bazel binary")


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse command line arguments

    Returns:
        A struct of parsed arguments.
    """
    parser = argparse.ArgumentParser("black fixer")

    parser.add_argument(
        "--bazel",
        type=Path,
        help="The path to a `bazel` binary. The `BAZEL_REAL` environment variable can also be used to set this value.",
    )
    parser.add_argument(
        "scope",
        nargs="*",
        default=["//...:all"],
        help="Bazel package or target scoping for formatting. E.g. `//...`, `//some:target`.",
    )

    parsed_args = parser.parse_args(args)

    if not parsed_args.bazel:
        parsed_args.bazel = find_bazel()

    return parsed_args


def query_targets(query_string: str, bazel: Path, workspace_dir: Path) -> List[str]:
    """Query python sources of bazel targets to run isort on

    Args:
        query_string: A query string to pass to `bazel query`.
        bazel: The path to a Bazel binary.
        workspace_dir: The location fo the Bazel workspace root.

    Returns:
        A list of targets provided by `bazel query`.
    """
    query_result = subprocess.run(
        [
            str(bazel),
            "query",
            query_string,
            "--noimplicit_deps",
            "--keep_going",
        ],
        cwd=str(workspace_dir),
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=False,
    )

    targets = query_result.stdout.splitlines()
    return targets


def run_black(
    sources: List[str],
    settings_path: Path,
    workspace_dir: Path,
) -> None:
    """Run black on a given set of sources

    Args:
        sources: A list of source targets to format.
        settings_path: The path to the isort config file.
        workspace_dir: The Bazel workspace root.
    """
    if not sources:
        return

    black_args = ["--config", str(settings_path)]

    if "RULES_BLACK_DEBUG" in os.environ:
        black_args.append("--verbose")

    black_args.extend(sources)

    exit_code = 0
    old_argv = list(sys.argv)
    sys.argv = [sys.argv[0]] + black_args
    old_cwd = os.getcwd()
    os.chdir(workspace_dir)
    try:
        black.patched_main()

    except SystemExit as exc:
        if exc.code is None:
            exit_code = 0
        elif isinstance(exc.code, str):
            exit_code = int(exc.code)
        else:
            exit_code = exc.code
    finally:
        os.chdir(old_cwd)
        sys.argv = old_argv

    if exit_code != 0:
        sys.exit(exit_code)


def pathify(label: str) -> str:
    """Converts //foo:bar into foo/bar."""
    if label.startswith("@"):
        raise ValueError("external label unsupported", label)
    if label.startswith("//:"):
        return label[3:]
    return label.replace(":", "/").replace("//", "")


def main() -> None:
    """The main entry point"""
    args = parse_args()

    if "BUILD_WORKSPACE_DIRECTORY" not in os.environ:
        raise EnvironmentError(
            "BUILD_WORKSPACE_DIRECTORY is not set. Is the process running under Bazel?"
        )

    workspace_dir = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])

    runfiles = Runfiles.Create()
    if not runfiles:
        raise EnvironmentError(
            "RUNFILES_MANIFEST_FILE and RUNFILES_DIR are not set. Is python running under Bazel?"
        )

    settings = _rlocation(runfiles, os.environ["BLACK_SETTINGS_PATH"])

    # Query explanation:
    # Filter all local targets ending in `*.py`.
    #     Get all source files.
    #         Get direct dependencies from targets matching the given scope.
    #         Except for targets tag to ignore formatting
    query_template = r"""filter("^//.*\.py$", kind("source file", deps(set({scope}) except attr(tags, "(^\[|, )(noformat|no-format|no-black-format)(, |\]$)", set({scope})), 1)))"""  # pylint: disable=line-too-long

    # Query for all sources
    targets = query_targets(
        query_string=query_template.replace("{scope}", " ".join(args.scope)),
        bazel=args.bazel,
        workspace_dir=workspace_dir,
    )

    sources = [pathify(t) for t in targets]

    run_black(
        sources=sources,
        settings_path=settings,
        workspace_dir=workspace_dir,
    )


if __name__ == "__main__":
    main()
