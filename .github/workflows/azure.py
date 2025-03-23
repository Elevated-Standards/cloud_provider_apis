import os
import json
from pathlib import Path

def is_openapi_spec(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return "info" in content and "paths" in content
    except Exception:
        return False

def extract_api_info_from_specs(specs_root, output_file):
    count = 0
    with open(output_file, 'w', encoding='utf-8') as out:
        for namespace_dir in Path(specs_root).glob('specification/*'):
            provider_name = namespace_dir.name

            # Look for any JSON file in resource-manager folders
            for json_file in namespace_dir.glob('**/resource-manager/**/*.json'):
                if not is_openapi_spec(json_file):
                    continue

                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
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
                        for method in methods:
                            out.write(f"- {method.upper()} {path}\n")
                    out.write("--------------------------------------------------------------------------------\n")
                    count += 1
                except Exception as e:
                    out.write(f"❌ Failed to parse {json_file}: {e}\n")
                    out.write("--------------------------------------------------------------------------------\n")

    print(f"✅ Parsed and wrote {count} service definitions to {output_file}")

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
