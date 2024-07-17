#!/bin/bash

API_URL="http://localhost:18000/add-image"
IMAGES_ROOT_DIR="resources/images"
MAX_CONCURRENT_JOBS=10

upload_image() {
  local artist="$1"
  local image_path="$2"
  local filename=$(basename "$image_path")

  local encoded_artist=$(echo "$artist" | jq -sRr @uri)

  echo "Uploading $image_path as $artist..."

  curl -X POST "${API_URL}?name=${encoded_artist}" \
       -H "accept: application/json" \
       -H "Content-Type: multipart/form-data" \
       -F "image=@$image_path"
}

wait_for_jobs() {
  while [[ $(jobs -r -p | wc -l) -ge $MAX_CONCURRENT_JOBS ]]; do
    sleep 1
  done
}

for artist_dir in "$IMAGES_ROOT_DIR"/*; do
  if [[ -d "$artist_dir" ]]; then
    artist=$(basename "$artist_dir")
    for image_path in "$artist_dir"/*.jpg; do
      if [[ -f "$image_path" ]]; then
        wait_for_jobs
        upload_image "$artist" "$image_path" &
      fi
    done
  fi
done

wait

echo "All images have been uploaded."
