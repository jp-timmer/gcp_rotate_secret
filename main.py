#!/usr/bin/env python
import google_crc32c
import string
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

# [START secretmanager_add_secret_version]
def add_secret_version(event, context):
    """
    Add new randomly generated secret version to the secret.
    """

    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("GCP_PROJECT_ID")
    secret_id = os.getenv("GCP_SECRET_ID")
    
    parent = client.secret_path(project_id, secret_id)
    payload = generate_random_string(30)
    payload = payload.encode("UTF-8")
    print('Payload: {}'.format(payload))
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

# [START secretmanager_generate_random_string]
def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    passwords = ''.join(secrets.choice(alphabet) for i in range(length))
    print ("Generated password of ", length, "is:", passwords)
    return passwords
    # [END secretmanager_generate_random_string]