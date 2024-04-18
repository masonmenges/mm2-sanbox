from prefect import task, flow, get_run_logger
from pydantic import BaseModel
from typing import Union

from prefect.runner.storage import GitRepository
from prefect.deployments.runner import DeploymentImage

class MetadataConfig(BaseModel):
    cell_type: str
    post_embedding_transformation_label: str
    phenoservice_key: str
    raise_on_existing_transformation: bool = True
    group_label_for_benchmarking: Union[str, None] = None

@flow
def logging_flow_1(
    metadata: MetadataConfig,
) -> None:
    logger = get_run_logger()
    logger.info("TEST TEST Running benchmarking flow ...")
    logger.info("TEST TEST Finished running benchmarking flow.")
    return None


@flow
def logging_flow_2(
    cell_type: str,
    post_embedding_transformation_label: str,
    phenoservice_key: str,
    raise_on_existing_transformation: bool = True,
    group_label_for_benchmarking: Union[str, None] = None,
) -> None:
    logger = get_run_logger()
    logger.info("TEST TEST Running benchmarking flow ...")
    logger.info("TEST TEST Finished running benchmarking flow.")

    return None


if __name__ == "__main__":

    logging_flow_1.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/debug_logging.py:logging_flow_1",
        ).deploy(
        name="logging_deployment_1",
        work_pool_name="k8s-minikube-test",
        version="local_demo_1",
        )
    logging_flow_2.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/debug_logging.py:logging_flow_2",
        ).deploy(
        name="logging_deployment_1",
        work_pool_name="k8s-minikube-test",
        version="local_demo_2",
        image=DeploymentImage(
                    name="masonm2/temprepo:demo_flow",
                    dockerfile="./Dockerfile",
                )
        )
