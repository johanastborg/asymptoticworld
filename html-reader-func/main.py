# main.py
import functions_framework
from google.cloud import storage

# Initialize the GCS client outside the function for efficiency
storage_client = storage.Client()

@functions_framework.http
def read_gcs_html(request):
    """
    HTTP Cloud Function that receives a list of GCS URIs in a JSON payload,
    reads the content of each file, and returns it.
    """
    # BigQuery remote UDFs send a POST request with a JSON body.
    # The structure is: {"calls": [[arg1_row1, arg2_row1, ...], [arg1_row2, ...]]}
    request_json = request.get_json(silent=True)
    replies = []
    calls = request_json['calls']

    for call in calls:
        try:
            gcs_uri = call[0] # The URI is the first (and only) argument
            if not gcs_uri or not gcs_uri.startswith('gs://'):
                # Handle invalid input gracefully
                replies.append(None)
                continue

            # Parse the GCS URI to get bucket and blob name
            bucket_name, blob_name = gcs_uri.replace('gs://', '').split('/', 1)

            # Get the bucket and blob
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # Download content as bytes and decode to a string (handle potential errors)
            html_content = blob.download_as_string().decode('utf-8', errors='ignore')
            replies.append(html_content)

        except Exception as e:
            # If any error occurs (e.g., file not found), return None for that row.
            # This prevents the entire query from failing.
            print(f"Error processing URI {call[0]}: {e}")
            replies.append(None)

    # The response must be a JSON object with a "replies" key.
    return {"replies": replies}
