import json
import pandas as pd
import requests
import os


def read_lines_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    return lines


def send_api_request(api_endpoint, request_data, headers, api_params={}):
    response = requests.post(
        api_endpoint, data=json.dumps(request_data), headers=headers, params=api_params
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
    return response.json()


def process_lines(lines, api_endpoint, headers={}, api_params={}):
    responses = []
    total_requests = len(lines)
    five_percent = total_requests // 20
    requested = 0
    reported = 0
    print(f"Sending {total_requests} requests.")
    for line in lines:
        request_data = json.loads(line)
        response = send_api_request(api_endpoint, request_data, headers, api_params)
        responses.append(response)
        requested += 1
        if requested % five_percent == 0:
            reported += 5
            print(
                f"{reported}%: {requested} requests sent. {total_requests - requested} remaining."
            )
    return responses


def main(input_file_name, output_file_name, api_endpoint, headers={}, params={}):
    lines = read_lines_from_file(input_file_name)
    responses = process_lines(lines, api_endpoint, headers, params)
    df = pd.DataFrame(responses)
    df.to_csv(output_file_name, index=False)
    print(f"Saved {len(df)} responses to {output_file_name}.")
    return df


if __name__ == "__main__":
    input_file_name = "input.txt"
    output_file_name = "output.csv"
    api_endpoint = "your endpoint here"
    headers = {"your headers: here"}
    params = {"your params: here"}
    df = main(input_file_name, output_file_name, api_endpoint, headers, params)
    print(df)
