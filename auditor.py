import boto3
import json
from botocore.exceptions import ClientError
from colorama import Fore, Style
from tabulate import tabulate

s3 = boto3.client('s3')
buckets = s3.list_buckets().get('Buckets', [])

results = []

def is_public_policy(policy_json):
    try:
        statements = policy_json.get("Statement", [])
        for stmt in statements:
            principal = stmt.get("Principal")
            effect = stmt.get("Effect")
            if principal == "*" and effect == "Allow":
                return True
    except:
        pass
    return False

def get_bucket_audit(bucket_name):
    public_policy = False
    acl_public = False
    block_public_access = True

    # BlockPublicAccess check
    try:
        config = s3.get_public_access_block(Bucket=bucket_name)
        settings = config['PublicAccessBlockConfiguration']
        block_public_access = all(settings.values())
    except ClientError as e:
        block_public_access = False  # Assume risky if we can't verify

    # Bucket Policy check
    try:
        policy_str = s3.get_bucket_policy(Bucket=bucket_name)['Policy']
        policy_json = json.loads(policy_str)
        public_policy = is_public_policy(policy_json)
    except ClientError:
        pass

    # ACL check
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        for grant in acl.get("Grants", []):
            grantee = grant.get("Grantee", {})
            if grantee.get("URI") in [
                "http://acs.amazonaws.com/groups/global/AllUsers",
                "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
            ]:
                acl_public = True
    except ClientError:
        pass

    return public_policy, acl_public, block_public_access

print(f"\n🔍 Auditing {len(buckets)} S3 bucket(s)...\n")

for bucket in buckets:
    name = bucket['Name']
    public_policy, acl_public, bpa = get_bucket_audit(name)

    is_risky = public_policy or acl_public or not bpa
    status = f"{Fore.RED}❌ Risky{Style.RESET_ALL}" if is_risky else f"{Fore.GREEN}✅ Safe{Style.RESET_ALL}"

    results.append([
        name,
        "Yes" if public_policy else "No",
        "Yes" if acl_public else "No",
        "Yes" if bpa else "No",
        status
    ])

# Print table
print(tabulate(
    results,
    headers=["Bucket Name", "Public Policy", "ACL Public", "BlockPublicAccess", "Status"]
))
