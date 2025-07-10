# import sys, os

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

# del sys, os

from localhelpers.create_secrets import slugify

# from helpers.secrets.create_secrets import slugify

from prefect import flow, task

@flow
def create_secrets_flow():
    secret_slug = slugify("!@#%!#$!798y79823y54")
    print(secret_slug)


if __name__ == "__main__":
    create_secrets_flow()