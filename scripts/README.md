# scripts/

Personal training scripts for the robot-competition portfolio.

## analyze_mic_log.py

Parses the serial log of the ESP32 + INMP441 microphone unit test and
summarizes quiet vs. speaking frames.

- Input: a text log with one frame per line, e.g.
  `peak=468 avg=373 start=2300 silence=1800 voice=0`
- Output: frame count, peak / average range for quiet and speaking groups,
  voice-on ratio, and a threshold sanity conclusion.
- Dependencies: Python 3 standard library only (`re`, `sys`, `os`).
- Sample data: `mic_log_sample.txt` (recorded 2026-11-25, classic ESP32
  Dev Module, INMP441, 8 kHz sample rate).

### Run

```bash
python analyze_mic_log.py                 # uses the sample file
python analyze_mic_log.py path/to/log.txt # parse your own log
```

Related unit test: PR #2 in the team repository
(https://github.com/AAC927/SEA/pull/2).
