#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Check if DJANGO_SETTINGS_MODULE is set.
if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
  echo "Error: DJANGO_SETTINGS_MODULE is not set. Please export it before running the script."
  exit 1
fi

# Check if the Django app name is provided as a command-line argument; if not, prompt the user.
if [ -z "$1" ]; then
  read -p "Enter the Django app name: " app_name
else
  app_name=$1
fi

# Change directory to the specified Django app.
if [ -d "$app_name" ]; then
  cd "$app_name" || { echo "Failed to change directory to $app_name"; exit 1; }
else
  echo "Error: Directory '$app_name' does not exist."
  exit 1
fi

# Dynamically set PYTHONPATH to include the current working directory.

# Get the current directory.
current_dir=$(pwd)

# If PYTHONPATH is not set, initialize it with the current directory.
if [ -z "$PYTHONPATH" ]; then
  export PYTHONPATH="$current_dir"
else
  # Check if the current directory is already in PYTHONPATH.
  case ":$PYTHONPATH:" in
    *":$current_dir:"*)
      # Already included; do nothing.
      ;;
    *)
      export PYTHONPATH="$PYTHONPATH:$current_dir"
      ;;
  esac
fi

echo "PYTHONPATH is set to: $PYTHONPATH"

# Run the django-admin compilemessages command for Farsi locale,
django-admin compilemessages --settings=volleyball_platform.settings
