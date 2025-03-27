#!/bin/bash

# Get the Cloud Run URL
SERVICE_URL=$(gcloud run services describe mc-verify-api --platform managed --region us-central1 --format 'value(status.url)')

echo "Testing Cloud Run service at: $SERVICE_URL"
echo "----------------------------------------"

echo -e "\n1. Testing MC Verification (Valid MC):"
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"mc_number": "551149"}' \
  $SERVICE_URL/verify_mc

echo -e "\n\n2. Testing MC Verification (Invalid MC):"
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"mc_number": "999999"}' \
  $SERVICE_URL/verify_mc

echo -e "\n\n3. Checking Status (Valid MC):"
curl $SERVICE_URL/status/551149

echo -e "\n\n4. Checking Status (Invalid MC):"
curl $SERVICE_URL/status/999999

echo -e "\n\n5. Listing All Verified MCs:"
curl $SERVICE_URL/verified_mcs

echo -e "\n\n6. Looking up Valid Load:"
curl $SERVICE_URL/loads/REF09460

echo -e "\n\n7. Looking up Invalid Load:"
curl $SERVICE_URL/loads/INVALID123

echo -e "\n\nTests completed!" 