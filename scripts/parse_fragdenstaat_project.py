"""This script downloads all requests from https://fragdenstaat.de/projekt/klimaschutz-und-klimaanpassungskonzepte/ """

import json
import re
from collections import namedtuple
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

# a regular expression that finds valid URLs in message contents, from https://urlregex.com/
EXTERNAL_URL_REGEX = (
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)

PDF_NAME_REGEX = r"/([^/]*\.pdf)"

# http content types for compressed files
COMPRESSION_FORMATS = [
    "application/gzip",
    "application/vnd.rar",
    "application/x-7z-compressed",
    "application/zip",
    "application/x-tar",
]

# http content types for images
IMAGE_FORMATS = [
    "image/bmp",
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/svg+xml",
    "image/tiff",
    "image/webp",
]

# http content types for text files
TEXT_FORMATS = ["application/rtf", "text/plain"]

HeaderInfo = namedtuple(
    "HeaderInfo",
    [
        "Content_Length",
        "Content_Type",
        "Content_Category",
        "Content_Disposition_Exists",
        "Error_Message",
    ],
)


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
    """Read the request responses and summarize the messages and attachments of each request in tables.
    Also look for URLs in the messages."""

    result_dataframe = None
    attachments_dataframe = None
    urls_dict = []

    for request_filepath in tqdm.tqdm(
        list((FILE_BASE_PATH / "requests").glob(("*.json")))
    ):
        # load the request
        with open(request_filepath, "r", encoding="utf-8") as f:
            request_content = json.load(f)

        # get the messages
        for message in request_content["messages"]:
            # filter for the relevant keys
            new_row = {key: message[key] for key in MESSAGE_RELEVANT_KEYS}

            # add the request id to the row
            new_row["request_id"] = request_content["id"]

            # look for URLs in the message
            regex_result = find_urls_in_message(request_content["id"], message)
            if len(regex_result["urls"]) > 0:
                for url in regex_result["urls"]:
                    url["header_info"] = summarize_url_header(url["url"])._asdict()

                urls_dict.append(regex_result)

            # add the number of found URLs
            new_row["url_count"] = len(regex_result)

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

    with open(FILE_BASE_PATH / "urls.json", "w", encoding="utf-8") as f:
        json.dump(urls_dict, f, indent=4, ensure_ascii=False)


def find_urls_in_message(request_id: int, message: dict) -> dict:
    """Find all URLs in a message and return a dict with the URLs and the message/request ids

    Args:
        request_id (int): The request id
        message (dict): The message, which has a key "content" and a key "id"

    Returns:
        dict: A dict with the URLs and the message/request ids
    """

    # look for URLs in the message
    regex_result = re.findall(EXTERNAL_URL_REGEX, message["content"])

    # ignore frag den staat URLs
    regex_result = [
        result
        for result in regex_result
        if not result.startswith("https://fragdenstaat.de")
    ]

    # collect in a dict
    return {
        "request_id": int(request_id),
        "message_id": int(message["id"]),
        "urls": [{"url_id": i, "url": url} for i, url in enumerate(regex_result)],
    }


def summarize_url_header(url: str) -> HeaderInfo:
    """Request the header of a URL and return a HeaderInfo object, containing Content Length and
    Type, Type category, Disposition Extras and error messages
    Original from https://stackoverflow.com/questions/65797228/how-to-check-if-a-url-is-downloadable-in-requests
    """

    try:
        headers = requests.head(url).headers
    except Exception as e:
        print(f"Could not get header information for {url}")
        return HeaderInfo(
            Content_Length=None,
            Content_Type=None,
            Content_Category=None,
            Content_Disposition_Exists=None,
            Error_Message=str(e),
        )

    Content_Length = [
        value for key, value in headers.items() if key == "Content-Length"
    ]
    if len(Content_Length) > 0:
        Content_Length = int("".join(map(str, Content_Length)))
    else:
        Content_Length = 0

    Content_Disposition_Exists = bool(
        {key: value for key, value in headers.items() if key == "Content_Disposition"}
    )
    if Content_Disposition_Exists is True:
        # TODO do something with the file, but this almost never happens
        return HeaderInfo(
            Content_Length=Content_Length,
            Content_Type=None,
            Content_Category=None,
            Content_Disposition_Exists=Content_Disposition_Exists,
            Error_Message=None,
        )
    else:
        # determine the content type
        Content_Type = list(
            {value for key, value in headers.items() if key == "Content-Type"}
        )

        Content_Category = None

        if any(
            [
                file_format
                for file_format in COMPRESSION_FORMATS
                if file_format in Content_Type
            ]
        ):
            Content_Category = "compressed"

        elif any(
            [
                file_format
                for file_format in IMAGE_FORMATS
                if file_format in Content_Type
            ]
        ):
            Content_Category = "image"

        elif any(
            [file_format for file_format in TEXT_FORMATS if file_format in Content_Type]
        ):
            Content_Category = "text"

        elif "application/pdf" in Content_Type:
            Content_Category = "pdf"

        elif "text/csv" in Content_Type:
            Content_Category = "csv"

        return HeaderInfo(
            Content_Length=Content_Length,
            Content_Type=Content_Type,
            Content_Category=Content_Category,
            Content_Disposition_Exists=Content_Disposition_Exists,
            Error_Message=None,
        )


def download_files():
    """Download files from the URLs in the attachments and message contents."""

    # create target folder
    target_folder = FILE_BASE_PATH / "files"
    target_folder.mkdir(parents=True, exist_ok=True)

    ## ATTACHMENTS
    print("Downloading attachments...")
    # read the dataframe
    attachments_dataframe = pd.read_csv(FILE_BASE_PATH / "attachments.csv")

    # iterate over the dataframe
    for _, row in tqdm.tqdm(
        attachments_dataframe.iterrows(), total=len(attachments_dataframe)
    ):
        # get the url
        url = row["file_url"]
        file_path = target_folder / f"a_{row['id']}_{row['name']}"

        # skip if file already exists
        if file_path.exists():
            continue

        # download the file
        try:
            response = requests.get(url, stream=True)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8096):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
        except Exception as e:
            print(f"Could not download file {url}")
            print(str(e))

    ## MESSAGES
    print("Downloading files from messages...")
    # read the json
    url_dicts = json.load(open(FILE_BASE_PATH / "urls.json", "r", encoding="utf-8"))

    # iterate over the dict
    for url_dict in tqdm.tqdm(url_dicts):
        message_id = url_dict["message_id"]

        for url_info in url_dict["urls"]:
            url_id = url_info["url_id"]
            url = url_info["url"]

            # try to determine the file name from the URL
            file_names = re.findall(
                PDF_NAME_REGEX,
                url,
                flags=re.IGNORECASE,
            )
            if len(file_names) > 0:
                file_name = file_names[-1]
            else:
                file_name = ""
            file_path = target_folder / f"m_{message_id}_{url_id}_{file_name}.pdf"

            # skip if file already exists
            if file_path.exists():
                continue

            # skip if error happened
            Error_Message = url_info["header_info"]["Error_Message"]
            if Error_Message is not None:
                continue

            # skip if not a pdf
            Content_Category = url_info["header_info"]["Content_Category"]
            if Content_Category != "pdf":
                continue

            # download the file
            try:
                response = requests.get(url, stream=True)
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8096):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
            except Exception as e:
                print(f"Could not download file {url}")
                print(str(e))


if __name__ == "__main__":
    download_raw_requests()
    summarize_messages()
    download_files()
