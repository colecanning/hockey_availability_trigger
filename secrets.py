# Import the Secret Manager client library.
from google.cloud import secretmanager_v1beta1 as secretmanager


# [START secretmanager_get_secret]
def get_secret(project_id, secret_id):
    """
    Get information about the given secret. This only returns metadata about
    the secret container, not any secret material.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)
    print(name)


    # Get the secret.
    response = client.get_secret(name)
    exit()

#     # Get the replication policy.
#     if response.replication.automatic:
#         replication = 'AUTOMATIC'
#     elif response.replication.user_managed:
#         replication = 'MANAGED'
#     else:
#         raise 'Unknown replication {}'.format(response.replication)

#     # Print data about the secret.
#     print('Got secret {} with replication policy {}'.format(
#         response.name, replication))
# # [END secretmanager_get_secret]

#     return response


print(get_secret("780728492658", "TestSecret"))
