import json
from datetime import datetime

import requests

tenant = "DEFAULT"
controller_id = "Device01"
auth_token = "c50218d2fb994c13a32e2402156e2297"
should_download = True
should_finish_update = True
update_exception = False


def get_with_token(url):
    return requests.get(url, headers={'Authorization': 'TargetToken {}'.format(auth_token)})


response = get_with_token(f'http://localhost:8080/{tenant}/controller/v1/{controller_id}')

print(response.status_code)
print(response.json())

print("-----------")

links = response.json()["_links"]

print("The following links are found")
for key in links:
    print(key + " -> " + str(links[key]["href"]))

print("-----------")

# Check if there is deploymentBase
if "deploymentBase" in links:
    print("Should do an update")
    downloadLink = links["deploymentBase"]["href"]
    print("Download link: " + downloadLink)
    response = get_with_token(downloadLink)
    payload = response.json()
    print(payload)
    action_id = payload["id"]
    print(f'Id of action: {action_id}')
    deployment = payload["deployment"]
    print(f'Download: {deployment["download"]}')
    print(f'Update: {deployment["update"]}')
    chunks = deployment["chunks"]
    for chunk in chunks:
        print(chunk)
        print(f'Chunk name: {chunk["name"]}, version {chunk["version"]}, part: {chunk["part"]}')
        artifacts = chunk["artifacts"]
        for artifact in artifacts:
            print(artifact)
            print(f'Filename: {artifact["filename"]}')
            print(f'Hashes: {artifact["hashes"]}')
            print(f'Size: {artifact["size"]}')
            download_link = artifact["_links"]["download-http"]["href"]
            print(f'Download: {download_link}')
            # Download the File
            if should_download:
                file = get_with_token(download_link)
                print(file.content)
                # Signal that the Update is finished!
                if should_finish_update:
                    if update_exception:
                        result = "failure"
                    else:
                        result = "success"
                    response_payload = json.dumps({"id": action_id, "time": datetime.now().strftime('%Y%m%dT%H%M%S'),
                                                   "status": {"result": {"finished": result}, "execution": "closed"},
                                                   "details": "The update worked like a charm"})
                    print(response_payload)
                    post_response = requests.post(
                        f'http://localhost:8080/{tenant}/controller/v1/{controller_id}/deploymentBase/{action_id}/feedback',
                        headers={'Authorization': 'TargetToken {}'.format(auth_token),
                                 'Content-Type': 'application/json', 'Accept': 'application/json'}, data=response_payload)
                    print(post_response.status_code)
                    print(post_response.content)
else:
    print("No Update scheduled")
