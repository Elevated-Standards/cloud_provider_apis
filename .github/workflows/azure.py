import os
import json
from pathlib import Path

def extract_api_info_from_specs(specs_root, output_file):
    count = 0
    with open(output_file, 'w') as out:
        for namespace_dir in Path(specs_root).glob('specification/*'):
            provider_name = namespace_dir.name
            resource_paths = list(namespace_dir.glob('**/resource-manager/**/*/swagger.json'))
            
            for swagger_path in resource_paths:
                try:
                    with open(swagger_path, 'r') as f:
                        spec = json.load(f)

                    info = spec.get("info", {})
                    title = info.get("title", "Unknown")
                    version = info.get("version", "Unknown")
                    paths = spec.get("paths", {})
                    
                    out.write(f"Service Name        : {title}\n")
                    out.write(f"API Version         : {version}\n")
                    out.write(f"Resource Provider   : {provider_name}\n")
                    out.write("Operations:\n")
                    for path, methods in paths.items():
                        for method in methods.keys():
                            out.write(f"- {method.upper()} {path}\n")
                    out.write("--------------------------------------------------------------------------------\n")
                    count += 1
                except Exception as e:
                    out.write(f"Failed to parse {swagger_path}: {e}\n")
                    out.write("--------------------------------------------------------------------------------\n")
    print(f"✅ Wrote {count} Azure service API specs to {output_file}")

def main():
    specs_root = "azure-rest-api-specs"
    output_file = "azure_services.txt"

    if not os.path.exists(specs_root):
        print("❌ Missing Azure REST API Specs repo. Please clone it:")
        print("git clone https://github.com/Azure/azure-rest-api-specs.git")
        return

    extract_api_info_from_specs(specs_root, output_file)

if __name__ == "__main__":
    main()
