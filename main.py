from IntentRetriever import IntentRetriever

if __name__ == '__main__':
    clu_key = input("Enter your CLU key: ")
    intentRetriever = IntentRetriever(clu_key)
    while (query := input("Enter your query: ")) != "quit":
        intentRetriever.retrieve_intent(query)
