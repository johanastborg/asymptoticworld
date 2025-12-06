#!/bin/bash
set -e

# Configuration:
# BUCKET: The name of the Google Cloud Storage bucket to mount
# MNT_DIR: The directory where the bucket will be mounted in the container
MNT_DIR=${MNT_DIR:-/mnt/gcs_bucket}

echo "Mounting GCS Bucket: $BUCKET to $MNT_DIR"

mkdir -p $MNT_DIR

# Mount the bucket using gcsfuse.
# We use --debug_gcs and --debug_fuse for troubleshooting (optional)
# --implicit-dirs is important if the bucket wasn't created with folders explicitly
# Run in background
gcsfuse --debug_gcs --debug_fuse --implicit-dirs $BUCKET $MNT_DIR &
PID=$!

# Wait for the mount to be ready
echo "Waiting for mount..."
# Simple wait loop
tries=0
while [ ! -d "$MNT_DIR" ] || [ -z "$(ls -A $MNT_DIR)" ] && [ $tries -lt 10 ]; do
    # Note: listing an empty bucket might return empty, but checking if dir exists and is a mountpoint is harder without mount command
    # A better check might be just sleep a bit or check if the process is still running
    sleep 1
    tries=$((tries+1))
done

# Check if gcsfuse is still running
if ! kill -0 $PID > /dev/null 2>&1; then
    echo "gcsfuse failed to start."
    exit 1
fi

echo "Mounting completed (or timed out waiting for content, proceeding anyway)."

# Start Gunicorn
# Bind to 0.0.0.0:$PORT
echo "Starting Gunicorn..."
exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app
