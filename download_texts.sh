#!/bin/bash

# Create the data directory if it doesn't exist
mkdir -p ./data

# Define the download URLs
urls=(
  "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
  "https://www.gutenberg.org/cache/epub/1513/pg1513.txt"
  "https://www.gutenberg.org/cache/epub/2701/pg2701.txt"
  "https://www.gutenberg.org/cache/epub/145/pg145.txt"
  "https://www.gutenberg.org/cache/epub/84/pg84.txt"
)

# Download each file
for url in "${urls[@]}"; do
  filename=$(basename "$url")  # Extract filename from URL
  wget -q -O "./data/$filename" "$url"  # Download file quietly and save with filename
  if [ $? -eq 0 ]; then
    echo "Downloaded: $filename"
  else
    echo "Error downloading: $url"
  fi
done

echo "Download completed."
