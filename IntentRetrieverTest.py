import pytest
from unittest.mock import patch
from IntentRetriever import IntentRetriever
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
import pytest

@pytest.fixture
def intent_retriever():
    # random clu key tests shouldnt pass
    return IntentRetriever("13124142132131")

def test_retrieve_intent(intent_retriever):
    query = "How do I make a chocolate cake?"
    expected_output = {
        "query": "How do I make a chocolate cake?",
        "top_intent": "recipe",
        "category": "cooking",
        "confidence_score": 0.95
    }

    with patch("azure.ai.language.conversations.ConversationAnalysisClient") as mock_client:
        mock_client.return_value.analyze_conversation.return_value = {
            "result": {
                "query": expected_output["query"],
                "prediction": {
                    "topIntent": expected_output["top_intent"],
                    "intents": [
                        {
                            "category": expected_output["category"],
                            "confidenceScore": expected_output["confidence_score"]
                        }
                    ]
                }
            }
        }

        intent_retriever.retrieve_intent(query)

        mock_client.assert_called_once_with(
            "https://testapi.cognitiveservices.azure.com/",
            AzureKeyCredential("13124142132131")
        )
        mock_client.return_value.analyze_conversation.assert_called_once_with(
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
                "parameters": {
                    "projectName": "TestAPI",
                    "deploymentName": "TextAnalyticsCreate-20240321232411",
                    "verbose": True
                }
            }
        )

        captured = capsys.readouterr()
        assert f"query: {expected_output['query']}" in captured.out
        assert f"top intent: {expected_output['top_intent']}" in captured.out
        assert f"category: {expected_output['category']}" in captured.out
        assert f"confidence score: {expected_output['confidence_score']}" in captured.out