# Build for Shyftlabs
# Script Author : Saurabh Kumar Jain
# Designation : Security Engineer
# Description : The script uses aws cli to connect with AWS Environment and then fetches all the bucket details
# It iterates each bucket policy and check if any of the bucket has public access

import json
import subprocess
from tabulate import tabulate
from termcolor import colored

def run_aws_cli(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout, None

def list_s3_buckets():
    output, error = run_aws_cli("aws s3api list-buckets --query 'Buckets[].Name' --output json")
    if error:
        print(colored(f" Failed to list buckets: {error}", "red"))
        return []
    return json.loads(output) if output else []

# Logic behind the bucket policy Check
def check_public_policy(bucket_name):
    output, error = run_aws_cli(f"aws s3api get-bucket-policy --bucket {bucket_name} --output json")
    if error:
        return "ERROR"
    try:
        policy_json = json.loads(output)["Policy"]
        policy = json.loads(policy_json)
        for statement in policy.get("Statement", []):
            principal = statement.get("Principal", {})
            effect = statement.get("Effect", "")
            if (principal == "*" or principal.get("AWS") == "*") and effect == "Allow":
                return "YES"
    except Exception:
        return "ERROR"
    return "NO"

def main():
    print("Scanning all S3 buckets for public access exposure...\n")
    buckets = list_s3_buckets()
    results = []
    total_buckets = 0
    public_count = 0
    private_count = 0
    error_count = 0

    for bucket in buckets:
        total_buckets += 1
        status = check_public_policy(bucket)

        if status == "YES":
            public_count += 1
            display = colored("Yes", "green")
        elif status == "NO":
            private_count += 1
            display = colored("No", "red")
        else:
            error_count += 1
            display = colored("Error", "yellow")

        print(f"{bucket} scanned successfully")
        results.append([bucket, display])

    # Display results table
    print("\n Final Results:\n")
    print(tabulate(results, headers=["Bucket Name", "Public Access"], tablefmt="fancy_grid"))

    # Summary
    print("\n Summary:")
    print(f" Total Buckets Scanned: {total_buckets}")
    print(colored(f" Public Buckets: {public_count}", "green"))
    print(colored(f" Private Buckets: {private_count}", "red"))
    print(colored(f" Buckets with Errors: {error_count}", "yellow"))

if __name__ == "__main__":
    main()

