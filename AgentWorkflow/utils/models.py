# AgentWorkflow/utils/models.py
from dotenv import load_dotenv, find_dotenv
import os
from AgentWorkflow.utils.aws_bedrock_llm import AWSBedrockLLM

load_dotenv(find_dotenv())

# Get AWS credentials and endpoint from your environment variables.
aws_endpoint = os.getenv("BEDROCK_ENDPOINT_NAME")
aws_region = os.getenv("AWS_REGION", "us-west-2")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_ACCESS_SECRET_KEY_ID")

# Instantiate the AWSBedrockLLM and assign it to `llm`
llm = AWSBedrockLLM(
    endpoint_name=aws_endpoint,
    aws_region=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)