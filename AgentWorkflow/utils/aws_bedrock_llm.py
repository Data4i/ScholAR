# AgentWorkflow/utils/aws_bedrock_llm.py
import boto3
import json
from typing import List, Optional
from langchain.llms.base import LLM

class AWSBedrockLLM(LLM):
    """
    Custom LLM wrapper for AWS Bedrock.
    """
    def __init__(self, endpoint_name: str, aws_region: str, aws_access_key_id: str, aws_secret_access_key: str, **kwargs):
        self.endpoint_name = endpoint_name
        self.aws_region = aws_region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.client = boto3.client(
            "sagemaker-runtime",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        # Any other parameters you want to support can be added as instance variables.

    @property
    def _llm_type(self) -> str:
        return "aws_bedrock"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Build your payload according to your Bedrock endpoint requirements.
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 7000,
                "temperature": 0.5,
                "top_k": 50,
                "top_p": 0.9,
                "num_return_sequences": 1,
                "do_sample": True,
            },
        }
        json_payload = json.dumps(payload)

        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType="application/json",
            Body=json_payload
        )
        response_body = json.loads(response["Body"].read().decode())
        # Extract and return the generated text.
        # Adjust this extraction logic based on your endpoint's response format.
        return response_body[0]["generated_text"]

    def predict(self, prompt: str, **kwargs) -> str:
        return self._call(prompt, stop=kwargs.get("stop"))