
from osdu_api.providers.aws.partition_info_aws import PartitionInfoAws

# Example response from partition service:
# {
#     "tenantSSMPrefix": {
#         "sensitive": false,
#         "value": "/osdu/<prefix>/shared"
#     },
#     "policy-service-enabled": {
#         "sensitive": false,
#         "value": "false"
#     },
#     "tenantId": {
#         "sensitive": false,
#         "value": "shared"
#     },
#     "resourcePrefix": {
#         "sensitive": false,
#         "value": "<prefix>"
#     },
#     "id": {
#         "sensitive": false,
#         "value": "osdu"
#     }
# }

def convert(content: dict) -> PartitionInfoAws:
    """Convert response from partition service to python object

    Args:
        content (dict): json response from partition service

    Returns:
        PartitionInfoAws: has attributes defining partition info
    """
    return PartitionInfoAws(
        content["id"]["value"],
        content["tenantId"]["value"],
        content["resourcePrefix"]["value"],
        content["tenantSSMPrefix"]["value"]
    )
    