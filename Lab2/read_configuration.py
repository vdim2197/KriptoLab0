import json


def read_configuration(file_path):
    try:
        with open(file_path, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data["encryption_algorithm"], config_data["key"]
    except FileNotFoundError:
        print("Config file not found.")
        return None, None
    except json.JSONDecodeError:
        print("Error decoding JSON in the config file.")
        return None, None


def read():

    config_file_path = "D:\Egyetem\harmadev\ElsoFelev\Kriptografia\KriptoLab0\Lab2\configuration.json"

    encryption_algorithm, key = read_configuration(config_file_path)

    if encryption_algorithm and key:
        print(f"Encryption Algorithm: {encryption_algorithm}")
        print(f"Key: {key}")
        return encryption_algorithm, key
    else:
        print("Failed to read configuration.")
