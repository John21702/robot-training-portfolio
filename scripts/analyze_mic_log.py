#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_mic_log.py

Parse an INMP441 microphone unit-test serial log and summarize the
quiet / speaking frames.

Log line format (one frame per line, comments start with '#'):
    peak=468 avg=373 start=2300 silence=1800 voice=0

Usage:
    python analyze_mic_log.py mic_log_sample.txt
    python analyze_mic_log.py            # reads mic_log_sample.txt next to this file

Only the Python standard library is used (re, sys, os). No third-party
package is required.
"""

import os
import re
import sys

# Matches one "key=value" pair, e.g. peak=468
PAIR_RE = re.compile(r"(\w+)=(-?\d+)")


def parse_line(line):
    """Return a dict of integer fields for one log line, or None to skip it."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    fields = {}
    for key, value in PAIR_RE.findall(line):
        fields[key] = int(value)

    # A real audio frame must carry at least peak, avg and voice.
    if "peak" not in fields or "avg" not in fields or "voice" not in fields:
        return None
    return fields


def summarize_group(name, frames):
    """Print min/max/count for one group and return nothing."""
    if not frames:
        print(f"{name:>10}: no frames")
        return

    peaks = [f["peak"] for f in frames]
    avgs = [f["avg"] for f in frames]
    print(f"{name:>10}: {len(frames):3d} frames | "
          f"peak {min(peaks):5d}-{max(peaks):5d} | "
          f"avg  {min(avgs):5d}-{max(avgs):5d}")


def main():
    # Resolve the log file: command-line argument, otherwise the sample next
    # to this script.
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    else:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "mic_log_sample.txt")

    if not os.path.isfile(log_path):
        print(f"[error] log file not found: {log_path}")
        sys.exit(1)

    quiet = []
    speaking = []

    with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            frame = parse_line(line)
            if frame is None:
                continue
            if frame["voice"] == 1:
                speaking.append(frame)
            else:
                quiet.append(frame)

    total = len(quiet) + len(speaking)
    print(f"Source log : {os.path.basename(log_path)}")
    print(f"Total frames parsed: {total}")
    print("-" * 60)
    summarize_group("quiet", quiet)
    summarize_group("speaking", speaking)
    print("-" * 60)

    if total:
        ratio = 100.0 * len(speaking) / total
        print(f"Voice-on frames: {len(speaking)}/{total} ({ratio:.1f}%)")

    # Simple sanity check: speaking frames should generally have larger peak
    # values than quiet frames.
    if quiet and speaking:
        quiet_max = max(f["peak"] for f in quiet)
        speak_min = min(f["peak"] for f in speaking)
        if speak_min > quiet_max:
            print("Conclusion: threshold separates quiet and speaking frames.")
        else:
            print("Conclusion: ranges overlap; check thresholds or noise floor.")


if __name__ == "__main__":
    main()
