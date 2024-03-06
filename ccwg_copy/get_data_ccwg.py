import requests
import argparse

# Constants
API_URL = "https://ecrimex.net/api/v1/cryptocurrency-addresses/{}"
OUTPUT_FILE = "first_valid_id.txt"


def get_response_status(id, bearer_token):
    """Check the response status for a given ID."""
    url = API_URL.format(id)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    return response.status_code


def exponential_find_upper_bound(bearer_token):
    """Find an upper bound for the valid ID range using exponential search."""
    id = 1
    while get_response_status(id, bearer_token) != 200:
        id *= 2
        if id > 1294886:  # Example upper limit, adjust as needed
            raise ValueError("Exceeded search limit during exponential find.")
    return id


def binary_search_for_first_valid_id(low, high, bearer_token):
    """Perform binary search to find the first valid ID."""
    first_valid_id = None
    while low <= high:
        mid = (low + high) // 2
        if get_response_status(mid, bearer_token) == 200:
            first_valid_id = mid
            high = mid - 1  # Narrow down the search towards lower IDs
        else:
            low = mid + 1  # Move towards higher IDs
    return first_valid_id


def save_id_to_file(id, file_path):
    """Save the found ID to a text file."""
    with open(file_path, "w") as file:
        file.write(str(id))


def main(bearer_token, output_file):
    upper_bound = exponential_find_upper_bound(bearer_token)
    first_valid_id = binary_search_for_first_valid_id(1, upper_bound, bearer_token)
    if first_valid_id:
        print(f"First valid ID found: {first_valid_id}")
        save_id_to_file(first_valid_id, output_file)
        print(f"First valid ID ({first_valid_id}) saved to {output_file}")
    else:
        print("Failed to find a valid ID.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the first valid ID with optimized HTTP requests and save it to a file."
    )
    parser.add_argument(
        "--bearer_token", required=True, help="Bearer token for API authentication."
    )
    parser.add_argument(
        "--output_file",
        default=OUTPUT_FILE,
        help="File path for saving the first valid ID.",
    )
    args = parser.parse_args()

    main(args.bearer_token, args.output_file)
