import logging

import requests
from giza import API_HOST
from giza.client import DeploymentsClient, WorkspaceClient

logger = logging.getLogger(__name__)


def get_workspace_uri():
    """
    Retrieves the URI of the current workspace.

    This function creates a WorkspaceClient instance using the API_HOST and
    calls its get method to retrieve the current workspace. It then returns
    the URL of the workspace.

    Returns:
        str: The URL of the current workspace.
    """
    client = WorkspaceClient(API_HOST)
    try:
        workspace = client.get()
    except requests.exceptions.RequestException:
        logger.error("Failed to retrieve workspace")
        logger.error(
            "Please check that you have create a workspaces using the Giza CLI"
        )
        raise
    return workspace.url


def get_deployment_uri(model_id: int, version_id: int):
    """
    Get the deployment URI associated with a specific model and version.

    Args:
        model_id (int): The ID of the model.
        version_id (int): The ID of the version.

    This function initializes a DeploymentsClient instance using the API_HOST and
    retrieves the deployment URI using its list method. The resulting URL of the
    deployment is returned.

    Returns:
        str: The URI of the deployment.
    """
    client = DeploymentsClient(API_HOST)
    deployments_list = client.list(model_id, version_id)

    deployments = deployments_list.root

    if deployments:
        return deployments[0].uri
    else:
        return None
