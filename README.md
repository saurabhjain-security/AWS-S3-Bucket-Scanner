# 🔐 S3 Public Access Scanner

A Python CLI tool to audit and detect **publicly accessible Amazon S3 buckets** in your AWS account using AWS CLI.

---

## 🚀 Features

- Lists all S3 buckets in your account
- Checks bucket **policies** for public access
- Detects:
  - Buckets allowing `"Principal": "*"` with `"Effect": "Allow"`
- Summarizes:
  - Total buckets scanned
  - Number of public, private, and failed-to-scan buckets
- Shows results in a clean **tabulated format**
- Highlights:
  - ✅ Public buckets in green
  - ❌ Private buckets in red
  - ⚠️ Errors in yellow

---

## 📦 Prerequisites

- Python 3.7+
- AWS CLI configured (`aws configure`)
- Required Python packages:
  ```bash
  pip install tabulate termcolor
