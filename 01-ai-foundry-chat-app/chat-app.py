import os

# Add references
from dotenv import load_dotenv
from urllib.parse import urlparse
from azure.identity import DefaultAzureCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        AZURE_AI_AGENT_ENDPOINT = os.getenv("AZURE_AI_AGENT_ENDPOINT")
        AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME =  os.getenv("AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME")

        # Get a chat client
        inference_endpoint = f"https://{urlparse(AZURE_AI_AGENT_ENDPOINT).netloc}/models"

        credential = DefaultAzureCredential(exclude_environment_credential=True,
                                            exclude_managed_identity_credential=True,
                                            exclude_interactive_browser_credential=False)

        chat = ChatCompletionsClient(
                endpoint=inference_endpoint,
                credential=credential,
                credential_scopes=["https://ai.azure.com/.default"])


        # Initialize prompt with system message
        prompt=[
                SystemMessage("You are a helpful AI assistant that answers questions.")
            ]

        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue
            
            # Get a chat completion
            prompt.append(UserMessage(input_text))
            response = chat.complete(
                model=AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME,
                messages=prompt)
            completion = response.choices[0].message.content
            print(completion)
            prompt.append(AssistantMessage(completion))

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()