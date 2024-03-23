from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

class IntentRetriever:

    def __init__(self, clu_key):
        self.clu_key = clu_key
        self.project_name = "TestAPI"


    def retrieve_intent(self, query):
        clu_endpoint = "https://testapi.cognitiveservices.azure.com/"
        deployment_name = "TextAnalyticsCreate-20240321232411"

        client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(self.clu_key))
        with client:
            result = client.analyze_conversation(
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "en",
                            "text": query
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {  # This section should be directly under task
                        "projectName": self.project_name,
                        "deploymentName": deployment_name,
                        "verbose": True
                    }
                }
            )

        print(f"query: {result['result']['query']}")
        print(f"top intent: {result['result']['prediction']['topIntent']}")
        print(f"category: {result['result']['prediction']['intents'][0]['category']}")
        print(f"confidence score: {result['result']['prediction']['intents'][0]['confidenceScore']}\n")




