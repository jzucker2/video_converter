#!/usr/bin/env python

import subprocess
import argparse

# ffmpeg -i "input.mkv" -y -f mp4 -vcodec copy -ac 2 -c:a libfaac "output.m4v"