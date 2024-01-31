# import wmill
import asyncio
# import requests
import httpx
import sys


async def dispatch_workflow(token, owner, repo, workflow_id, ref, inputs={}):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    print(url)
    data = {
        'ref': ref,
        'inputs': inputs
    }
    try:
        # Using asyncio.to_thread to run the synchronous requests.post in a separate thread
        # response = await asyncio.to_thread(requests.post, url, headers=headers, json=data)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


async def run_dispatch(token, owner, repo, workflow_id, ref, inputs={}):
    response = await dispatch_workflow(token, owner, repo, workflow_id, ref, inputs)
    if response is None:
        print("Failed to dispatch workflow.")
        return None

    if response.status_code == 204:
        print("Success: Workflow dispatched, no content returned.")
    else:
        try:
            print(f"Status Code: {response.status_code}, Response JSON: {response.json()}")
        except ValueError:
            print(f"Status Code: {response.status_code}, Response Text: {response.text}")

    return response.status_code

# Example usage
# asyncio.run(run_dispatch(token, owner, repo, workflow_id, ref, inputs))


if __name__ == "__main__":
    token = "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"
    owner = "mehrdad-ordobadi"
    repo = "melo-3.0"
    workflow_id = "tf_apply_dispatch.yml"
    # workflow_id = "tf_destroy_dispatch.yml"
    ref = "env"
    inputs = {"env_name": sys.argv[1], "branch_name": "env"}
    asyncio.run(run_dispatch(token, owner, repo, workflow_id, ref, inputs))