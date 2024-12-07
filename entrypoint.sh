#!/bin/bash
if [ "$STORAGE_TYPE" = "MongoDB" ]; then
  echo "Starting MongoDB import..."
  mongoimport --db "$STORAGE_NAME" --collection "$STORAGE_COLLECTION" --file /data/data.json --jsonArray
else
  echo "STORAGE_TYPE is not MongoDB. Skipping import."
fi
mongod --bind_ip_all
