#!/usr/bin/env python
import google_crc32c
import string
import secrets
import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
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
    
    # [START update_db_password]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

    project = os.getenv("GCP_PROJECT_NAME")
    instance = os.getenv("GCP_INSTANCE_ID")
    name = os.getenv("GCP_USERNAME")
    host = "%"
    user_body = {
        "password": payload,
    }
    request = service.users().update(
        project=project, instance=instance, name=name, host=host, body=user_body)
    responsedb = request.execute()
    print(responsedb)
    # [END update_db_password]

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

# [START secretmanager_generate_random_string]
def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    passwords = ''.join(secrets.choice(alphabet) for i in range(length))
    return passwords
    # [END secretmanager_generate_random_string]
