import sys
import subprocess
import multiprocessing
import os
import yaml
import re

main_domain = sys.argv[1]
tmp_dir = "./tmp_results/"
tools_result = "./tools_extracted_result/"

def parse_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
        tools = {}
        for category, tool_list in config['tools'].items():
            for tool in tool_list:
                tool_name = tool['name']
                tool_command = tool['command'].format(domain=sys.argv[1])
                timeout = tool['timeout']
                tool_type = category
                tools[tool_name] = {'command': tool_command, 'timeout': timeout, 'type': tool_type}
        return tools
    

def altdns_parse_domains(result):
    # Split the result by newline characters
    lines = result.strip().split('\n')

    # Extract domains from each line
    domains = []
    for line in lines:
        parts = line.split(':')
        if len(parts) == 2:
            domains.append(parts[0])

    # Remove duplicates
    unique_domains = list(set(domains))

    return unique_domains


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
            with open(f"{tmp_dir}{output_file_path}", "w") as output_file:
                subprocess.run(tool_command, stdout=output_file, stderr=devnull, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"Command {tool_command} timed out. Continuing with the script...")

    with open(f"{tmp_dir}{output_file_path}", "r") as output_file:
        tool_output = output_file.read()

    result = extract_subdomains(main_domain, tool_output)

    result_file_path = f"{tools_result}{tool_name}_subdomains.txt"
    print(f'Creating file of {tool_name} in {result_file_path}')
    with open(result_file_path, "a") as result_file:
        for subdomain in result:
            result_file.write(subdomain + '\n')

    print(f"Subdomains originating from {main_domain} using {tool_name} have been saved to {result_file_path}")



def collect_domains_in_single_result_file():
    unique_domains = set()
    with open(f"{main_domain}_total_domains.txt", "a") as output_file:
        for tool_name, tool_info in tools.items():
            with open(f"{tools_result}{tool_name}_subdomains.txt", "r") as tool_output:
                for domain in tool_output:
                    if domain not in unique_domains:
                        output_file.write(domain)
                        unique_domains.add(domain)


def remove_color(text):
    # Define regex pattern to match ANSI escape codes for color formatting
    ansi_escape = re.compile(r'\033\[[0-9;]*m')

    # Remove ANSI escape codes from the text
    return ansi_escape.sub('', text)



def launch_subdomain_permutation(commands):
    for tool_name, command in commands.items():
        try:
            print(f'{tool_name} is running ... ')
            output = subprocess.run(command['command'], shell=True, check=True, capture_output=True, text=True)
            result = remove_color(output.stdout)
            # Process the result as needed
            result_file_path = f"{tools_result}{tool_name}_subdomains_permuted.txt"
            with open(result_file_path, "w") as result_file:
                domains = altdns_parse_domains(result)
                for domain in domains:
                    result_file.write(domain+"\n")
            print(f"Subdomains obtained from permutation using {tool_name} have been saved to {result_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {tool_name}: {e}")
            continue


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python script.py <domain>")
    #     sys.exit(1)
    config_file = "config.yaml"
    tools = parse_config(config_file)
    # processes = []
    # for tool_name, tool_info in tools.items():
    #     tool_command = tool_info['command']
    #     timeout = tool_info['timeout']
    #     tool_type = tool_info['type']
    #     output_file_tmp = f"{tool_name}_{main_domain}_tmp.txt"
    #     process = multiprocessing.Process(target=run_tool, args=(tool_name, tool_command.split(), output_file_tmp, timeout*60))
    #     processes.append(process)
    #     process.start()

    # for process in processes:
    #     process.join()
    # collect_domains_in_single_result_file()
    permutation_tools = {tool_name: tool_info for tool_name, tool_info in tools.items() if tool_info.get('type') == 'permutation'}
    print(permutation_tools)
    launch_subdomain_permutation(permutation_tools)