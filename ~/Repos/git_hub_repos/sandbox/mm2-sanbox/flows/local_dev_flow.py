from prefect import flow, runtime, get_run_logger



@flow
def check_flow_deployment_version():
    """
    This flow checks the version of the deployment
    """
    logger = get_run_logger()

    print(runtime.flow_run)

    if runtime.deployment.id:
        deployment_id = runtime.deployment.id
        logger.info(deployment_id)
    else:
        logger.info("No deployment id found")


if __name__ == "__main__":
    check_flow_deployment_version()
