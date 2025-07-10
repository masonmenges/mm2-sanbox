from prefect import settings
import numpy as np
import requests
import re
import json

def get_secrets_from_json(file_path: str) -> dict:
    """
    Read secrets from a JSON file and return them as a dictionary.
    
    Args:
        file_path: Path to the JSON file containing secrets
        
    Returns:
        Dictionary containing the secrets from the JSON file
    """
    try:
        with open(file_path, 'r') as f:
            secrets = json.load(f)
        return secrets
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found at path: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")


def slugify(text: str) -> str:
    """
    Convert a string into a URL-safe slug by replacing special characters.
    
    Args:
        text: The string to convert to a slug
        
    Returns:
        A URL-safe slug version of the input string
    """
    non_slug_characters = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]
    
    t_table = {ord(c): u'0' for c in non_slug_characters}

    # Convert to lowercase
    text = text.lower()
    text = text.replace(' ', '0')
    # Remove any non-slug characters using the translation table
    text = text.translate(t_table)
    # Remove any remaining non-alphanumeric characters except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def create_cloud2_secrets(
        secrets_file_path: str,
        api_key: str = None,
        api_url: str = None
        ) -> dict:
    """
    Creates secrets in Prefect Cloud 2 from a JSON file. Requires prefect 3.1 or greater to function correctly
    
    Args:
        secrets_file_path: Path to the JSON file containing secrets to create
        api_key: Optional Prefect Cloud API key. If not provided, uses local settings
        api_url: Optional Prefect Cloud API URL. If not provided, uses local settings
        
    Returns:
        a dictionary of key values pair with the original key mapped to the new key_slug
    """

    cur_settings = settings.get_current_settings()
    api = cur_settings.api
    
    if not api_url:
        api_url = api.url
    
    if not api_key:
        api_key = api.key.get_secret_value()


    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}",
    }

    block_request = requests.get(
                    url=f"{api_url}/block_types/slug/secret",
                    headers=headers,
                )
    block_request.raise_for_status()
    
    block_type_id = block_request.json()["id"]
    
    block_schema_id_request = requests.post(
                    url=f"{api_url}/block_schemas/filter",
                    headers=headers,
                    json={"block_schemas":{"block_type_id":{"any_":[block_type_id]}}}
                )
    
    block_schema_id_request.raise_for_status()

    block_schema_id = block_schema_id_request.json()[0]["id"]

    secrets = get_secrets_from_json(secrets_file_path)

    keys = list(secrets.keys())

    keys_splits = np.array_split(keys, 10)

    new_keys = {}
    failed_keys = {}

    for split in keys_splits:
        for key in split:
            key_slug = slugify(key)

            print(f"Creating secret for {key} using slug {key_slug}")

            try:
                r = requests.post(
                    url=f"{api_url}/block_documents/",
                    headers=headers,
                    json={"name":key_slug,
                        "block_schema_id":block_schema_id,
                        "block_type_id":block_type_id,
                        "data":{"value":secrets[key]}}
                )
                r.raise_for_status()
                new_keys[key] = key_slug
            except Exception as e :
                print(f"unable to create secret for {key} with exception \n {e}")
                failed_keys[key] = key_slug

    if failed_keys > 0:
        print(f"Secret creation failed for the following keys {failed_keys}")

    return new_keys


if __name__ == "__main__":
    # print(slugify("s()()/\/\/ome!@#$%@%$#@&$8798&*^*s%tring"))

    created_secrets = create_cloud2_secrets(secrets_file_path="misc/fake_secrets.json")
    print(f"{created_secrets}")
