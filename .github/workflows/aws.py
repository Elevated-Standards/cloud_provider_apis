import re
import botocore
import boto3

def parse_service_info(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    services = content.split('--------------------------------------------------------------------------------\n')
    service_info_list = []

    for service in services:
        if service.strip():
            service_info = {}
            service_info['Service Name'] = re.search(r'Service Name\s+:\s+(.+)', service).group(1)
            service_info['Service ID'] = re.search(r'Service ID\s+:\s+(.+)', service).group(1)
            service_info['API Version'] = re.search(r'API Version\s+:\s+(.+)', service).group(1)
            service_info['Endpoint Prefix'] = re.search(r'Endpoint Prefix\s+:\s+(.+)', service).group(1)
            operations = re.findall(r'-\s+(.+)', service)
            service_info['Operations'] = operations
            service_info_list.append(service_info)

    return service_info_list

def main():
    file_path = '/workspaces/cloud_provider_apis/aws_services.txt'
    service_info_list = parse_service_info(file_path)

    for service_info in service_info_list:
        print(f"Service Name: {service_info['Service Name']}")
        print(f"Service ID: {service_info['Service ID']}")
        print(f"API Version: {service_info['API Version']}")
        print(f"Endpoint Prefix: {service_info['Endpoint Prefix']}")
        print("Operations:")
        for operation in service_info['Operations']:
            print(f"  - {operation}")
        print("--------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
