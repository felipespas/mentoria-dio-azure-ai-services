from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from pathlib import Path

def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:

        # Get config settings
        load_dotenv()
        AZURE_AI_SEARCH_ENDPOINT = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
        AZURE_AI_SEARCH_KEY = os.getenv('AZURE_AI_SEARCH_KEY')
        AZURE_AI_SEARCH_INDEX_NAME_NO_VECTOR = os.getenv('AZURE_AI_SEARCH_INDEX_NAME_NO_VECTOR')

        # Get a search client
        search_client = SearchClient(AZURE_AI_SEARCH_ENDPOINT, AZURE_AI_SEARCH_INDEX_NAME_NO_VECTOR, AzureKeyCredential(AZURE_AI_SEARCH_KEY))

        user_inputs = [
            "London",
            "flights"
        ]

         # Loop until the user types 'quit'
        for user_input in user_inputs:
        
            print("----------------------------------------------------------------------------")
            print(f"\nSearching for: {user_input}")
            
            # Search the index
            found_documents = search_client.search(
                search_text=user_input,
                select=["metadata_storage_name", "locations", "people", "keyphrases"],
                order_by=["metadata_storage_name"],
                include_total_count=True
            )

            # Parse the results
            print(f"\nSearch returned {found_documents.get_count()} documents:")
            for document in found_documents:
                document_name = document["metadata_storage_name"]
                print(f"\nDocument: {document_name}")
                print(" - Locations:")
                for location in document["locations"]:
                    print(f"   - {location}")
                print(" - People:")
                for person in document["people"]:
                    print(f"   - {person}")
                print(" - Key phrases:")
                for phrase in document["keyphrases"]:
                    print(f"   - {phrase}")

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()        