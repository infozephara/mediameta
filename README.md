# mediafit

A small, dependency-free tool. It does two things:

1. **Media metadata** — reads metadata from a video/audio/image file.
2. **Runtime fingerprint** — prints a short block about the runtime.

## Why a runtime fingerprint?

Media pipelines behave differently depending on the runtime, so
mediafit prints a small block so you can confirm the environment.
It reads a few `/proc` entries and tries a couple of local
connections. That is all. Nothing to configure.

## Requirements

- Python 3.8+  (required)
- ffprobe     (optional)

## Install

    git clone https://github.com/USERNAME/mediafit.git /tmp/mediafit
    cd /tmp/mediafit
    sh install.sh

## Run

    python3 mediafit.py             # fingerprint
    python3 mediafit.py <file>     # media metadata + fingerprint

## Output

Saved to: `/mnt/user-data/outputs/mediafit-report.txt`