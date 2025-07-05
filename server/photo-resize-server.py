#!/usr/bin/python3

# requires 
#     sudo apt install libvips-tools
#

from flask import Flask, request, send_file, abort
import os
import subprocess
import time

from datetime import datetime

app = Flask(__name__)

PHOTO_DIR = "/var/www/slideshow/photos"
CACHE_DIR = "/var/cache/resized-photos"
LOG_FILE = os.path.join(os.path.dirname(__file__), "resize.log")
WRITE_TO_LOG = False

os.makedirs(CACHE_DIR, exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if WRITE_TO_LOG:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    else:
        print (f"[{timestamp}] {message}\n")


def is_ios9(user_agent):
    return "iPhone OS 9" in user_agent or "CPU OS 9" in user_agent

def resize_with_vips(src, dst):
    try:
        subprocess.run(
            ["vipsthumbnail", src, "-s", "1024x768", "-o", dst + "[Q=90]"],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        log(f"[ERROR] vipsthumbnail failed: {e}")
        return False


@app.route("/photos/<filename>")
def serve_image(filename):
    if ".." in filename or not filename.lower().endswith(".jpg"):
        log(f"Rejected suspicious filename: {filename}")
        return abort(400)

    ua = request.headers.get("User-Agent", "")
    is_ipad2 = is_ios9(ua)

    original_path = os.path.join(PHOTO_DIR, filename)
    if not os.path.exists(original_path):
        log(f"File not found: {filename}")
        return abort(404)

    if is_ipad2:
        cached_path = os.path.join(CACHE_DIR, filename)
        if os.path.exists(cached_path):
            log(f"Served cached resized image: {filename}")
            return send_file(cached_path, mimetype="image/jpeg")

        start = time.monotonic()

        try:
            if resize_with_vips(original_path, cached_path):
                duration = time.monotonic() - start
                log(f"Resized for iPad 2 via libvips: {filename} {duration:.2f}s")
                return send_file(cached_path, mimetype="image/jpeg")
            else:
                return abort(500)
        except Exception as e:
            log(f"[ERROR] Resize failed for {filename}: {e}")
            return abort(500)
    else:
        log(f"Served original image: {filename}")
        return send_file(original_path, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005)

