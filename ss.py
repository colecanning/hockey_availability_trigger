from google.cloud import secretmanager_v1beta1 as secretmanager

secrets = secretmanager.SecretManagerServiceClient()
projectid = "587789046371"


ALPHA_VANTAGE_KEY = secrets.access_secret_version("projects/"+projectid+"/secrets/alpha-vantage-key/versions/1").payload.data.decode("utf-8")

print(ALPHA_VANTAGE_KEY)
