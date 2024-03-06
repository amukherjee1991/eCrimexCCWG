import requests
import json
import sys
import csv

def get_command_line_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <BearerToken> <OutputCSVFileName>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def build_headers(token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

def build_initial_payload():
    return {
        "filters": {
            "createdAt": {
                "from": 1362627971,
                "to": 1709757102
            }
        },
        "sorts": [
            {
                "sortBy": "createdAt",
                "sortOrder": "asc",
                "limit":100
            }
        ]
    }

def process_data(data, csv_writer):
    for item in data['data']:
        item['metadata'] = json.dumps(item.get('metadata', {}))
        item.pop('notes', None)
        csv_writer.writerow(item)

def get_next_page_url(data):
    # Adjust this based on your API's actual response structure for pagination
    return data.get('next_page')

def fetch_all_pages(initial_url, headers, initial_payload, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=[
            'id', 'currency', 'source', 'discoveredAt', 'address', 'crimeCategory',
            'siteLink', 'price', 'email', 'confidence', 'createdAt', 'updatedAt',
            'status', 'procedure', 'actorCategory', 'metadata'
        ])
        csv_writer.writeheader()
        
        url = initial_url
        payload = json.dumps(initial_payload)
        while url:
            print(f"Fetching data from: {url}")
            if payload:
                response = requests.post(url, headers=headers, data=payload)
                payload = None  # Clear the payload after the first request
            else:
                # Ensure headers are included in subsequent GET requests
                response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                process_data(data, csv_writer)
                url = get_next_page_url(data)
            else:
                print(f"Failed to fetch data: HTTP {response.status_code}")
                break

def main():
    token, output_file = get_command_line_arguments()
    headers = build_headers(token)
    initial_payload = build_initial_payload()
    initial_url = "https://ecrimex.net/api/v1/cryptocurrency-addresses/search"
    
    fetch_all_pages(initial_url, headers, initial_payload, output_file)
    print(f"Data has been saved to {output_file}")

if __name__ == "__main__":
    main()
