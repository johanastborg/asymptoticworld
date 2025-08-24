gcloud functions deploy read-gcs-html-udf \
  --project=$PROJECT \
  --region=$REGION \
  --gen2 \
  --runtime="python311" \
  --source="." \
  --entry-point="read_gcs_html" \
  --trigger-http \
  --allow-unauthenticated
