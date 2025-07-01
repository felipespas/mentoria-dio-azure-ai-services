import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        AZURE_AI_FOUNDRY_HUB_OPEN_AI_ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_HUB_OPEN_AI_ENDPOINT")
        AZURE_AI_FOUNDRY_HUB_OPEN_AI_KEY = os.getenv("AZURE_AI_FOUNDRY_HUB_OPEN_AI_KEY")
        AZURE_AI_FOUNDRY_HUB_CHAT_MODEL = os.getenv("AZURE_AI_FOUNDRY_HUB_CHAT_MODEL")
        AZURE_AI_FOUNDRY_HUB_EMBEDDING_MODEL = os.getenv("AZURE_AI_FOUNDRY_HUB_EMBEDDING_MODEL")
        AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        AZURE_AI_SEARCH_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
        AZURE_AI_SEARCH_INDEX_NAME = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")

        # Get an Azure OpenAI chat client
        chat_client = AzureOpenAI(
            api_version = "2024-12-01-preview",
            azure_endpoint = AZURE_AI_FOUNDRY_HUB_OPEN_AI_ENDPOINT,
            api_key = AZURE_AI_FOUNDRY_HUB_OPEN_AI_KEY
        )

        # Initialize prompt with system message
        prompt = [
            {"role": "system", "content": "You are a travel assistant that provides information on travel services available from Margie's Travel."}
        ]

        input_texts = [
            "what are the destinations offered by Margies?",
            "tell me more about New York",
            "what are the available tours in New York?"
        ]

        # Loop until the user types 'quit'
        for input_text in input_texts:
            print("--------------------------------------------------------------------")
            print(f"\nUser: {input_text}")

            # Add the user input message to the prompt
            prompt.append({"role": "user", "content": input_text})

            # Additional parameters to apply RAG pattern using the AI Search index
            rag_params = {
                "data_sources": [
                    {
                        # he following params are used to search the index
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": AZURE_AI_SEARCH_ENDPOINT,
                            "index_name": AZURE_AI_SEARCH_INDEX_NAME,
                            "authentication": {
                                "type": "api_key",
                                "key": AZURE_AI_SEARCH_KEY,
                            },
                            # The following params are used to vectorize the query
                            "query_type": "vector",
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": AZURE_AI_FOUNDRY_HUB_EMBEDDING_MODEL,
                            },
                        }
                    }
                ],
            }

            # Submit the prompt with the data source options and display the response
            response = chat_client.chat.completions.create(
                model=AZURE_AI_FOUNDRY_HUB_CHAT_MODEL,
                messages=prompt,
                extra_body=rag_params
            )
            completion = response.choices[0].message.content
            print(f"Assistant: {completion}")

            # print the references from the response
            if response.choices[0].message.model_extra['context']['citations']:
                print("References:")
                for source in response.choices[0].message.model_extra['context']['citations']:
                    print(f"- title: {source['title']})")

            # Add the response to the chat history
            prompt.append({"role": "assistant", "content": completion})

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()