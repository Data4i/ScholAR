import os
import sys

# Append the project root to sys.path to allow package imports to work correctly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Import our custom AWSBedrockLLM class.
from AgentWorkflow.utils.aws_bedrock_llm import AWSBedrockLLM

# Get AWS credentials and endpoint from your environment variables.
aws_endpoint = os.getenv("BEDROCK_ENDPOINT_NAME")
aws_region = os.getenv("AWS_REGION", "us-west-2")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")

aws_secret_access_key = os.getenv("AWS_ACCESS_SECRET_KEY_ID")

# Check that credentials are set
if aws_endpoint is None:
    raise ValueError("BEDROCK_ENDPOINT_NAME is not set in environment variables.")
if aws_access_key_id is None:
    raise ValueError("AWS_ACCESS_KEY_ID is not set in environment variables.")
if aws_secret_access_key is None:
    raise ValueError("AWS_SECRET_ACCESS_KEY is not set in environment variables.")

# Instantiate the AWSBedrockLLM and assign it to `llm`
llm = AWSBedrockLLM(
    endpoint_name=aws_endpoint,
    aws_region=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

