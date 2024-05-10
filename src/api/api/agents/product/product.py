import os
import json
from typing import Dict, List
import prompty
from openai import AzureOpenAI
import pathlib
from product.ai_search import retrieve_documentation
from promptflow.tools.common import init_azure_openai_client
from promptflow.connections import AzureOpenAIConnection
from promptflow.core import (AzureOpenAIModelConfiguration, Prompty, tool)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

def get_context(question, embedding):
    return retrieve_documentation(question=question, index_name="product-info", embedding=embedding)


def get_embedding(question: str):
    connection = AzureOpenAIConnection(        
                    azure_deployment=os.environ["AZURE_EMBEDDING_NAME"],
                    api_key=os.environ["AZURE_OPENAI_API_KEY"],
                    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
                    api_base=os.environ["AZURE_OPENAI_ENDPOINT"]
                    )
                
    client = init_azure_openai_client(connection)

    return client.embeddings.create(
            input=question,
            model=os.environ["AZURE_EMBEDDING_NAME"]
        ).data[0].embedding


def get_products(context: str) -> Dict[str, any]:
    embedding = get_embedding(context)
    products = get_context(context, embedding)
    print(products)
    return products


if __name__ == "__main__":
    context = "Can you use a selection of tents and backpacks as context?"
    answer = get_products(context)
    print(json.dumps(answer, indent=2))
