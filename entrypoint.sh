#!/bin/sh
set -e

# Entry point ensures upload dir exists and correct ownership, then drops privileges if started as root.

UPLOAD_DIR="${UPLOAD_FOLDER:-/data/uploads}"

# Ensure upload dir exists
mkdir -p "$UPLOAD_DIR"

# If running as root, fix ownership and drop to appuser
if [ "$(id -u)" = '0' ]; then
  # Try to chown (ignore failure)
  chown -R appuser:appgroup "$UPLOAD_DIR" || true
  chmod 2770 "$UPLOAD_DIR" || true

  # If gosu is available, run the command as appuser
  if command -v gosu >/dev/null 2>&1; then
    exec gosu appuser /bin/sh -c 'exec "$@"' -- "$@"
  else
    # Fallback to su -c (less ideal)
    exec su -s /bin/sh appuser -c 'exec "$@"' -- "$@"
  fi
else
  # Already non-root, run directly
  exec /bin/sh -c 'exec "$@"' -- "$@"
fi
