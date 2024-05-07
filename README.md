# AWS Resource Discovery

<img src="logo.png" alt="Logo">

This tool is designed to interact with AWS and list resources such as EC2 instances, S3 buckets, IAM users, and more. It provides a web interface where users can select which resources they want to view.

## Features

- List AWS resources
- Interactive web interface and a Terminal-Based Version
- Supports multiple AWS profiles

This AWSPECT app is particularly crucial for [Terraform](terraform.io) users, especially when they face issues like a lost or corrupted `tfstate` file. This file is essential as it tracks the state of AWS resources managed by Terraform. Losing this file can leave users without clear insight into their AWS environments.

**Key Benefits:**

1. **Resource Synchronization:** Helps identify and reconcile AWS resources if the Terraform state is lost, ensuring accurate infrastructure management.
2. **Visibility and Audit:** Provides an independent check on AWS resources, which is essential for compliance and cost management.
3. **Disaster Recovery:** Assists in quickly identifying active AWS resources, facilitating faster recovery operations.
4. **Verification of Infrastructure Changes:** Verifies that Terraform changes have been properly implemented in AWS, adding an extra layer of assurance.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.6 or higher
- pip3
- AWS CLI installed and configured (optional, for testing AWS credentials locally)

## Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/awspect.git
   cd awspect
   ```

2. **Set up a Python virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the requirements**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Set up AWS Credentials**

   Make sure your AWS credentials are configured. If you haven't done so, run:

   ```bash
   aws configure
   ```

   This will prompt you to enter your AWS Access Key ID, Secret Access Key, region, and output format.

## Configuration

The tool uses the default AWS profile by default. You can set a different profile by modifying the `.env` file:

```python
AWS_PROFILE=default
```

## Usage

Install the requirements.txt file:

```bash
pip3 install -r requirements.txt

python3 awspect-web.py
```

Visit `http://127.0.0.1:5000/` in your web browser to use the tool.

---

`NOTE:If you prefer to use the terminal-based version of this application, follow the instructions below:`

## Running the Terminal-Based Version

This version of the application allows you to discover and list AWS resources directly within your terminal. Execute the following command to run it:

```bash
python3 awspect-terminal.py
```

This command launches the script that interacts with AWS to retrieve and display resources in the command line interface.

## Contributing

Contributions are welcome! Feel free to open pull requests or issues in the GitHub repository.
