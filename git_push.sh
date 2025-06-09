# Check if a commit message is provided
if [ -z "$1" ]; then
  echo "Error: Please provide a commit message."
  exit 1