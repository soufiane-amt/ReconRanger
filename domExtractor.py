import sys
import subprocess
import multiprocessing
import os
import yaml


def parse_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
        tools = {}
        for tool in config['tools']:
            tools[tool['name']] = [tool['command'].format(domain=sys.argv[1]), tool['timeout']]
        return tools

def extract_subdomains(input_domain, tool_output):
    subdomains = []
    for line in tool_output.split('\n'):
        if input_domain in line:
            parts = line.split()
            for part in parts:
                if part != input_domain and part.endswith(input_domain):
                    subdomains.append(part)
    return subdomains

def run_tool(tool_name, tool_command, output_file_path, timeout):
    with open(os.devnull, 'w') as devnull:
        try:
            print(f'{tool_name} is running ... ')
            with open(output_file_path, "w") as output_file:
                subprocess.run(tool_command, stdout=output_file, stderr=devnull, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"Command {tool_command} timed out. Continuing with the script...")

    with open(output_file_path, "r") as output_file:
        tool_output = output_file.read()

    result = extract_subdomains(sys.argv[1], tool_output)

    result_file_path = f"{tools_result}{tool_name}_subdomains.txt"
    print(f'Creating file of {tool_name} in {result_file_path}')
    with open(result_file_path, "w") as result_file:
        for subdomain in result:
            result_file.write(subdomain + '\n')

    print(f"Subdomains originating from {sys.argv[1]} using {tool_name} have been saved to {result_file_path}")

def collect_domains_in_single_result_file():
    unique_domains = set()
    with open(f"{sys.argv[1]}_total_domains.txt", "a") as output_file:
        for tool_name, tool_command in tools.items():
            with open(f"{tools_result}{tool_name}_subdomains.txt", "r") as tool_output:
                for domain in tool_output:
                    if domain not in unique_domains:
                        output_file.write(domain)
                        unique_domains.add(domain)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <domain>")
        sys.exit(1)

    tools_result = "./tools_extracted_result/"
    config_file = "config.yaml"
    main_domain = sys.argv[1]
    tools = parse_config(config_file)

    processes = []
    for tool_name, (tool_command, timeout) in tools.items():
        output_file_tmp = f"{tool_name}_{main_domain}_tmp.txt"
        process = multiprocessing.Process(target=run_tool, args=(tool_name, tool_command, output_file_tmp, timeout))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    collect_domains_in_single_result_file()
