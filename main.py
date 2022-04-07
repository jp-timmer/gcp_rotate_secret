#!/usr/bin/env python
import google_crc32c
import string
import secrets
import os
from dotenv import load_dotenv

# [START secretmanager_add_secret_version]
def add_secret_version(project_id, secret_id, payload):
    """
    Update the metadata about an existing secret.
    """

    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()

    parent = client.secret_path(project_id, secret_id)

    payload = payload.encode("UTF-8")

    crc32c = google_crc32c.Checksum()
    crc32c.update(payload)

    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": payload, "data_crc32c": int(crc32c.hexdigest(), 16)},
        }
    )

    print("Added secret version: {}".format(response.name))
    # [END secretmanager_add_secret_version]

    return response

if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv("GCP_PROJECT_ID")
    secret_id = os.getenv("GCP_SECRET_ID")
    alphabet = string.ascii_letters + string.digits
    passwords = ''.join(secrets.choice(alphabet) for i in range(30))

    add_secret_version(project_id, secret_id, passwords)