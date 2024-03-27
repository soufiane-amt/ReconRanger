import sys
import subprocess


main_domain = sys.argv[1]
tmp_dir = "./tmp_results/"

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

def run_tool(tool_command, output_file_path, timeout):
    try:
        with open(f"{tmp_dir}{output_file_path}", "w") as output_file:
            subprocess.run(tool_command, stdout=output_file, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"Command {tool_command} timed out. Continuing with the script...")


# Run different tools

for tool_name, tool_command in tools.items():
    output_file_tmp = f"{tool_name}_{main_domain}_tmp.txt"
    run_tool(tool_command, output_file_tmp, timeout=60*5)

    with open(f"{tmp_dir}{output_file_tmp}", "r") as output_file:
        tool_output = output_file.read()

    result = extract_subdomains(main_domain, tool_output)

    result_file_path = f"{tool_name}_subdomains.txt"
    with open(result_file_path, "w") as result_file:
        for subdomain in result:
            result_file.write(subdomain + '\n')

    print(f"Subdomains originating from {main_domain} using {tool_name} have been saved to {result_file_path}")
