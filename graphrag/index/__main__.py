# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""The Indexing Engine package root."""

import argparse
from enum import Enum

from .cli import index_cli


class ReporterType(Enum):
    """The type of reporter to run."""

    RICH = "rich"
    PRINT = "print"
    NONE = "none"

    def __str__(self):
        """Return the string representation of the enum value."""
        return self.value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        help="The root directory to use for input data and output data",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--config",
        help="The configuration yaml file to use when running the pipeline",
        # required if resume is not defined
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Runs the pipeline with verbose logging",
        action="store_true",
    )
    parser.add_argument(
        "--mem-profile",
        help="Runs the pipeline with memory profiling",
        action="store_true",
    )
    parser.add_argument(
        "--resume",
        help="Resume a given data run leveraging Parquet output files",
        # only required if config is not defined
        type=str,
    )
    parser.add_argument(
        "--reporter",
        help="The progress reporter to use.",
        type=ReporterType,
        choices=list(ReporterType),
    )
    parser.add_argument(
        "--emit",
        help="A comma-separated list of data formats to emit. Possible values: [parquet|csv] Default=parquet",
        type=str,
        default="parque",
    )
    parser.add_argument(
        "--dry-run",
        help="Run the pipeline without actually executing any steps and inspect the configuration",
        action="store_true",
    )
    parser.add_argument("--no-cache", help="Disable LLM cache.", action="store_true")
    parser.add_argument(
        "--init",
        help="Create an initial configuration in the given path",
        action="store_true",
    )
    parser.add_argument(
        "--overlay-defaults",
        help="Overlay default configuration values on a provided configuration file (--config)",
        action="store_true",
    )
    args = parser.parse_args()

    # validate arguments
    if args.overlay_defaults and not args.config:
        parser.error("--overlay-defaults requires --config")

    index_cli(
        root=args.root,
        verbose=args.verbose or False,
        resume=args.resume,
        memprofile=args.mem_profile or False,
        nocache=args.nocache or False,
        reporter=args.reporter,
        config=args.config,
        emit=args.emit,
        dryrun=args.dry_run or False,
        init=args.init or False,
        overlay_defaults=args.overlay_defaults or False,
        cli=True,
    )
