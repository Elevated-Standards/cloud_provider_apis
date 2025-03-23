import os
import botocore.session
from botocore.exceptions import UnknownServiceError, EndpointConnectionError

def get_regions_for_service(service_name):
    """
    Return all regions where a specific service is available.
    """
    session = botocore.session.get_session()
    try:
        resolver = session.get_component('endpoint_resolver')
        partitions = resolver.get_available_partitions()
        regions = set()
        for partition in partitions:
            service_regions = resolver.get_available_endpoints(service_name, partition)
            regions.update(service_regions)
        return sorted(regions)
    except Exception:
        return []

def write_service_doc_for_region(service_name, region_name, output_dir, session):
    """
    Writes API metadata for a service in a given region.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"service_{region_name}.txt")

    with open(file_path, 'w') as f:
        try:
            client = session.create_client(service_name, region_name=region_name)
            model = client.meta.service_model

            f.write(f"Service Name      : {model.service_name}\n")
            f.write(f"Service ID        : {model.service_id}\n")
            f.write(f"API Version       : {model.api_version}\n")
            f.write(f"Endpoint Prefix   : {model.endpoint_prefix}\n")
            f.write("Operations:\n")
            for op in sorted(model.operation_names):
                f.write(f"- {op}\n")
            f.write("--------------------------------------------------------------------------------\n")
        except EndpointConnectionError:
            f.write(f"⚠️ No endpoint in region {region_name}\n")
        except Exception as e:
            f.write(f"❌ Failed to load service '{service_name}' in region '{region_name}': {e}\n")
        f.write("--------------------------------------------------------------------------------\n")

def main():
    session = botocore.session.get_session()
    all_services = session.get_available_services()

    base_output_dir = "aws_service_docs"
    os.makedirs(base_output_dir, exist_ok=True)

    for service_name in sorted(all_services):
        print(f"🔍 Processing service: {service_name}")
        service_output_dir = os.path.join(base_output_dir, service_name)
        regions = get_regions_for_service(service_name)

        if not regions:
            print(f"⚠️ No available regions found for service: {service_name}")
            continue

        for region in regions:
            print(f"  🌍 Region: {region}")
            write_service_doc_for_region(service_name, region, service_output_dir, session)

if __name__ == "__main__":
    main()
