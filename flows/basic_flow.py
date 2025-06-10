from prefect import flow

from custom_block_edl import EnterpriseDataLake


@flow
def main():
    enterprisedatalake_block = EnterpriseDataLake.load("test-new-block")
    print(enterprisedatalake_block.upload())
    return True

main()