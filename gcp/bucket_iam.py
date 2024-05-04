import os
from google.cloud import storage
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


bucket_name = os.getenv("SOURCE_BUCKET")
role = "Owner"
member = "core@synavate.tech"


# ADD IAM MEMBER FOR GCS
def add_bucket_iam_member(bucket_name, role, member):
    """Add a new member to an IAM Policy"""
    
    

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    policy.bindings.append({"role": role, "members": {member}})

    bucket.set_iam_policy(policy)

    print(f"Added {member} with role {role} to {bucket_name}.")
    


#VIEW IAM MEMBER FOR GCS
def view_bucket_iam_members(bucket_name):
    """View IAM Policy for a bucket"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    for binding in policy.bindings:
        print(f"Role: {binding['role']}, Members: {binding['members']}")
        
#USE ON BUCKET
from google.cloud import storage


def add_bucket_conditional_iam_binding(
    bucket_name, role, title, description, expression, members
):
    """Add a conditional IAM binding to a bucket's IAM policy."""
    bucket_name = "your-bucket-name"
    role = "IAM role, e.g. roles/storage.objectViewer"
    members = {"IAM identity, e.g. user: "name@example.com"}
    # title = "Condition title."
    # description = "Condition description."
    # expression = "Condition expression."

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)

    # Set the policy's version to 3 to use condition in bindings.
    policy.version = 3

    policy.bindings.append(
        {
            "role": role,
            "members": members,
            "condition": {
                "title": title,
                "description": description,
                "expression": expression,
            },
        }
    )

    bucket.set_iam_policy(policy)

    print(f"Added the following member(s) with role {role} to {bucket_name}:")

    for member in members:
        print(f"    {member}")

    print("with condition:")
    print(f"    Title: {title}")
    print(f"    Description: {description}")
    print(f"    Expression: {expression}")
