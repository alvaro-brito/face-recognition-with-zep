#!/bin/bash

API_URL="http://localhost:18000/recognize"

TESTS_DIR="resources/tests"

recognize_image() {
  local image_path="$1"
  local filename=$(basename "$image_path")

  echo "Recognizing $image_path..."

  response=$(curl -s -X POST "$API_URL" \
       -F "image=@$image_path")

  echo "Response for $filename: $response"
}

for image_path in "$TESTS_DIR"/*.jpg; do
  if [[ -f "$image_path" ]]; then
    recognize_image "$image_path"
  fi
done

echo "All test images have been processed."
