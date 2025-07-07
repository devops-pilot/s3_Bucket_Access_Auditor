# 🔐 S3 Bucket Access Auditor

A Python CLI tool to **audit all S3 buckets** in your AWS account and detect **public access risks** via bucket policies, ACLs, and public access configurations.

---

## 🚀 Features

- ✅ Lists all S3 buckets in the account
- 🔍 Checks for:
  - Public bucket policies (`Principal: "*"`)
  - Public ACLs (`AllUsers`, `AuthenticatedUsers`)
  - Block Public Access (BPA) settings
- 🎨 Color-coded output to flag `❌ Risky` vs `✅ Safe` buckets
- 💡 No write permissions required — only `s3:Get*` access

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/s3-access-auditor.git
cd s3-access-auditor
```
### 2. (Optional but recommended) Create a virtual environment
```python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies 
```pip install -r requirements.txt
```
### 🧪 Usage

###### Make sure your AWS credentials are configured (via ~/.aws/credentials, environment variables, or IAM role).

```python auditor.py
```
## 📊 Sample Output
##### 🔍 Auditing 4 S3 bucket(s)...
```
| Bucket Name       | Public Policy | ACL Public | BlockPublicAccess | Status    |
|-------------------|---------------|-------------|--------------------|-----------|
| my-secure-bucket  | No            | No          | Yes                | ✅ Safe    |
| my-old-bucket     | Yes           | No          | No                 | ❌ Risky   |
| team-shared-data  | No            | Yes         | Yes                | ❌ Risky   |
```
## 🔐 IAM Permissions Required
##### Minimal read-only access:
```
{
  "Effect": "Allow",
  "Action": [
    "s3:ListAllMyBuckets",
    "s3:GetBucketPolicy",
    "s3:GetBucketAcl",
    "s3:GetPublicAccessBlock"
  ],
  "Resource": "*"
}
```
## 📁 Project Structure
```
s3-access-auditor/
├── auditor.py              # Main script
├── requirements.txt
├── .gitignore
└── README.md
```
## 📄 License
- MIT License

## 🙌 Contributions Welcome
- Feel free to fork, enhance, and submit PRs. If you find this tool helpful, drop a ⭐ on GitHub!