# GCP Rotate Secret for Cloud Functions

Simple Python script that helps rotate a secret on GCP.

Uses Python's built in `secrets` library to generate a random string of 30 characters.

## .env template
| Name  | Description  |  Example |
|---|---|---|
| GCP_PROJECT_ID | Project ID in numeric value |  12345678901 |
| GCP_SECRET_ID | Name of the secret |  testsecret |
