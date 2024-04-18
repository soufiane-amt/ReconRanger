# ReconRanger (Cybersecurity Reconnaissance Automation Tool)

## Overview

This tool is designed to automate various cybersecurity reconnaissance tasks, making bug bounty hunting and security research more efficient and effective. It leverages a combination of tools and techniques to gather information about a target domain, including subdomain discovery, DNS enumeration, and more.

### Features

- **Automated Reconnaissance**: Execute multiple reconnaissance tools with a single command.
- **Configurable**: Easily customize the tool by editing the YAML configuration file.
- **Subdomain Discovery**: Identify subdomains associated with the target domain.
- **Subdomain Permutation**: Generate potential subdomains based on permutations of the target domain.
- **Result Consolidation**: Combine the results of different reconnaissance tools into a single file.
- **Automated Screenshots**: Capture screenshots of active subdomains for visual analysis.

## Usage

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/cyber-recon-tool.git
    ```

### Configuration

Edit the `config.yaml` file to specify the reconnaissance tools to be used, along with their commands and timeouts.

### Running the Tool

Run the script with the target domain as a command-line argument:

```bash
python3.11 subdomain_discovery.py facebook.com
