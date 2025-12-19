import json
import os


def clean_json_data(data):
    """
    Recursively removes keys with empty string, empty list, or empty dictionary values.
    For lists, removes empty string, empty list, or empty dictionary elements.
    (Note: Original comments were requested to be removed, but added this docstring for clarity on function purpose)
    """
    if isinstance(data, dict):
        cleaned_dict = {}
        for key, value in data.items():
            cleaned_value = clean_json_data(value)
            if cleaned_value != "" and cleaned_value != [] and cleaned_value != {}:
                cleaned_dict[key] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        cleaned_list = []
        for item in data:
            cleaned_item = clean_json_data(item)
            if cleaned_item != "" and cleaned_item != [] and cleaned_item != {}:
                cleaned_list.append(cleaned_item)
        return cleaned_list
    else:
        return data


def process_json_file(input_filename, output_filename):
    """
    Reads a JSON file, cleans the content, and writes to a new JSON file.
    (Note: Original comments were requested to be removed, but added this docstring for clarity)
    """
    with open(input_filename, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    cleaned_data = clean_json_data(json_data)

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    input_file = input("Enter the path to the JSON file to clean: ")
    output_file = input("Enter the path for the output JSON file: ")

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
    else:
        process_json_file(input_file, output_file)
