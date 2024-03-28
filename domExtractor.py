import sys
import subprocess
import multiprocessing
import os

main_domain = sys.argv[1]
tmp_dir = "./tmp_results/"
tools_result = "./tools_extracted_result/"

tools = {
    "amass": ["amass", "enum", "-passive", "-d", main_domain],
    "subfinder": ["subfinder", "-d", main_domain],
    # Add more tools and their respective commands here
}

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
    # Create a temp file that contains the output with tool name's prefix 
    with open(os.devnull, 'w') as devnull:
        try:
            print(f'{tool_name} is running ... ')
            with open(f"{tmp_dir}{output_file_path}", "w") as output_file:
                subprocess.run(tool_command, stdout=output_file, stderr=devnull, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"Command {tool_command} timed out. Continuing with the script...")

    # Read the temp file , parse and extract domains
    with open(f"{tmp_dir}{output_file_path}", "r") as output_file:
        tool_output = output_file.read()

    result = extract_subdomains(main_domain, tool_output)

    result_file_path = f"{tools_result}{tool_name}_subdomains.txt"
    print(f'Creating file of {tool_name} in {result_file_path}')
    with open(result_file_path, "w") as result_file:
        for subdomain in result:
            result_file.write(subdomain + '\n')

    print(f"Subdomains originating from {main_domain} using {tool_name} have been saved to {result_file_path}")

def collect_domains_in_single_result_file():
    with open(f"{main_domain}_total_domains.txt", "a") as output_file:
        for tool_name, tool_command in tools.items():
            with open(f"{tools_result}{tool_name}_subdomains.txt", "r") as tool_ouput:
                output_file.write(tool_ouput.read())




if __name__ == "__main__":
    processes = []
    for tool_name, tool_command in tools.items():
        output_file_tmp = f"{tool_name}_{main_domain}_tmp.txt"
        process = multiprocessing.Process(target=run_tool, args=(tool_name, tool_command, output_file_tmp, 60*3))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    collect_domains_in_single_result_file()
