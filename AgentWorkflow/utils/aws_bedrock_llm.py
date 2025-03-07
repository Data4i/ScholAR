import boto3
import json
from typing import List, Optional
from langchain.llms.base import LLM
from pydantic import Field, PrivateAttr

class AWSBedrockLLM(LLM):
    endpoint_name: str = Field(..., description="Name of the Bedrock endpoint")
    aws_region: str = Field(..., description="AWS region for the endpoint")
    aws_access_key_id: str = Field(..., description="AWS access key ID")
    aws_secret_access_key: str = Field(..., description="AWS secret access key")
    _client: object = PrivateAttr()  # Private attribute for the boto3 client

    def __init__(self, endpoint_name: str, aws_region: str, aws_access_key_id: str, aws_secret_access_key: str, **kwargs):
        # Initialize the Pydantic model (LLM)
        super().__init__(
            endpoint_name=endpoint_name,
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            **kwargs
        )
        # Initialize the boto3 client and store it as a private attribute.
        client = boto3.client(
            "sagemaker-runtime",
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        object.__setattr__(self, "_client", client)

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
        response = self._client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType="application/json",
            Body=json_payload
        )
        response_body = json.loads(response["Body"].read().decode())
        # Adjust extraction logic based on your endpoint's response format.
        return response_body[0]["generated_text"]

    def predict(self, prompt: str, **kwargs) -> str:
        return self._call(prompt, stop=kwargs.get("stop"))
    
    def bind_tools(self, tool_classes):
        """
        Bind tools to the LLM. This method is required by some prebuilt agent workflows.
        """
        self.tool_classes = tool_classes
        return self
