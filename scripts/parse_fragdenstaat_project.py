"""This script downloads all requests from https://fragdenstaat.de/projekt/klimaschutz-und-klimaanpassungskonzepte/ """

import json
from pathlib import Path

import pandas as pd
import requests
import tqdm

# the base url of Frag den Staat
API_BASE_URL: str = "https://fragdenstaat.de/api/v1"

# the base path for all files
FILE_BASE_PATH: Path = Path("data/fragdenstaat")

# the keys from the message that should be in the dataframe
MESSAGE_RELEVANT_KEYS = [
    "id",
    "sent",
    "is_response",
    "is_postal",
    "kind",
    "is_escalation",
    "status",
    "timestamp",
    "sender",
    "status_name",
]

# the keys from the attachments that should be in the dataframe
ATTACHMENT_RELEVANT_KEYS = [
    "id",
    "name",
    "filetype",
    "pending",
    "approved",
    "redacted",
    "is_pdf",
    "is_image",
    "is_irrelevant",
    "site_url",
    "anchor_url",
    "file_url",
]


def download_raw_requests():
    """Get the list of requests and then download each request and save the results as files"""
    result_objects = []

    # get the list of requests
    requests_url = f"{API_BASE_URL}/request?project=278"

    while requests_url:
        # get the list of requests
        response = requests.get(requests_url)

        # check if the request was successful
        if response.status_code != 200:

            raise Exception(f"Request failed with status code {response.status_code}")

        # parse content as dict
        parsed_content = json.loads(response.content)

        # iterate over all requests
        result_objects += parsed_content["objects"]

        # get the next url
        requests_url = parsed_content["meta"]["next"]

    # write to file
    if not FILE_BASE_PATH.exists():
        FILE_BASE_PATH.mkdir(parents=True)
    with open(FILE_BASE_PATH / "raw_requests_list.json", "w", encoding="utf-8") as f:
        json.dump(result_objects, f, indent=4, ensure_ascii=False)

    # go through all requests and get the detail of each request
    for result_object in tqdm.tqdm(result_objects):
        # get the resource_uri
        resource_uri = result_object["resource_uri"]

        # download the request
        response = requests.get(resource_uri)

        # check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        # parse content as dict
        parsed_content = json.loads(response.content)

        # save the reponse as file
        if not (FILE_BASE_PATH / "requests/").exists():
            not (FILE_BASE_PATH / "requests/").mkdir()
        with open(
            FILE_BASE_PATH / "requests" / f"{parsed_content['id']}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(parsed_content, f, indent=4, ensure_ascii=False)


def summarize_messages():
    """Read the request responses and summarize the messages and attachments of each request in tables"""

    result_dataframe = None
    attachments_dataframe = None

    for request_filepath in (FILE_BASE_PATH / "requests").glob(("*.json")):
        # load the request
        with open(request_filepath, "r", encoding="utf-8") as f:
            request_content = json.load(f)

        # get the messages
        for message in request_content["messages"]:
            # filter for the relevant keys
            new_row = {key: message[key] for key in MESSAGE_RELEVANT_KEYS}

            # add the request id to the row
            new_row["request_id"] = request_content["id"]

            if result_dataframe is None:
                # create dataframe
                result_dataframe = pd.DataFrame(new_row, index=[0])
            else:
                # add the row to the dataframe
                result_dataframe = result_dataframe.append(new_row, ignore_index=True)

            # get the attachments
            for attachment in message["attachments"]:
                new_row = {key: attachment[key] for key in ATTACHMENT_RELEVANT_KEYS}

                # add the message id to the row
                new_row["message_id"] = message["id"]

                # add the request id to the row
                new_row["request_id"] = request_content["id"]

                if attachments_dataframe is None:
                    # create dataframe
                    attachments_dataframe = pd.DataFrame(new_row, index=[0])
                else:
                    # add the row to the dataframe
                    attachments_dataframe = attachments_dataframe.append(
                        new_row, ignore_index=True
                    )

    # change the ids to int
    result_dataframe["id"] = result_dataframe["id"].astype(int)
    result_dataframe["request_id"] = result_dataframe["request_id"].astype(int)

    attachments_dataframe["id"] = attachments_dataframe["id"].astype(int)
    attachments_dataframe["message_id"] = attachments_dataframe["message_id"].astype(
        int
    )
    attachments_dataframe["request_id"] = attachments_dataframe["request_id"].astype(
        int
    )

    # write to file
    result_dataframe.to_csv(FILE_BASE_PATH / "messages.csv", index=False)
    attachments_dataframe.to_csv(FILE_BASE_PATH / "attachments.csv", index=False)

    # write as json
    result_dataframe.to_json(
        FILE_BASE_PATH / "messages.json", orient="records", indent=4
    )
    attachments_dataframe.to_json(
        FILE_BASE_PATH / "attachments.json", orient="records", indent=4
    )


if __name__ == "__main__":
    download_raw_requests()
    summarize_messages()
