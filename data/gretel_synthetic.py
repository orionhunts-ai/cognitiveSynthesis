"""
Gretel Synthetic data generated from the cyber threat intelligence dataset.
Note: Executed in a local container environment or GCP
- Type of model:

"""
import os
from dotenv import load_dotenv, find_dotenv
from gretel_client import create_project, poll
from gcp_upload import upload_blob
load_dotenv(find_dotenv())
from file_logger import setup_logger

#Config logger
logger = setup_logger()

def init_gretel_project(config):
    project = create_project("Threat-Intelligence-Synthesis")
    
    GCP_DATA_FOLDER=f"{os.getenv("SOURCE_BUCKET")}/{os.getenv("SOURCE_PATH")}"
    GCP_DATA_FILE = f"{os.getenv("SOURCE_BUCKET")}/{os.getenv("SOURCE_FILE")}"
    GRETEL_PROJECT_NAME="Threat-Intelligence-Synthesis"

    if project is None:
        project = create_project(GRETEL_PROJECT_NAME)
    else:
        pass
        logger("Project already exists", project.project)
    
    if model_config == False:
        model_config == "synthetics/default"
        
    

    # create a synthetic model using a default synthetic config from
    #   https://github.com/gretelai/gretel-blueprints/blob/main/config_templates/gretel/synthetics/default.yml
    #
    #   Providing a data_source will override the datasource from the template. If the data source is a local
    #   file, then it will automatically be uploaded to Gretel Cloud as part of the submission step
    model = project.create_model_obj(
        model_config=,
        data_source=GCP_DATA_SOURCE
    )

    # submit the model to Gretel Cloud for training
    model.submit()

    # wait for the model to training
    poll(model)

    # read out a preview data from the synthetic model
    pd.read_csv(model.get_artifact_link("data_preview"), compression="gzip")