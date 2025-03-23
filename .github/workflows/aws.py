import botocore.session

def main():
    file_path = 'aws_services.txt'
    session = botocore.session.get_session()
    available_services = session.get_available_services()

    with open(file_path, 'w') as f:
        for service_name in sorted(available_services):
            try:
                client = session.create_client(service_name)
                model = client.meta.service_model

                f.write(f"Service Name      : {model.service_name}\n")
                f.write(f"Service ID        : {model.service_id}\n")
                f.write(f"API Version       : {model.api_version}\n")
                f.write(f"Endpoint Prefix   : {model.endpoint_prefix}\n")
                f.write("Operations:\n")
                for op in sorted(model.operation_names):
                    f.write(f"- {op}\n")
                f.write("--------------------------------------------------------------------------------\n")
            except Exception as e:
                f.write(f"❌ Failed to load service '{service_name}': {e}\n")
                f.write("--------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
