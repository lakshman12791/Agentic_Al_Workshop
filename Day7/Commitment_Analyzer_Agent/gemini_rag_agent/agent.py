# gemini_rag_agent/agent.py

class GeminiRAGAgent:
    def __init__(self, retriever=None, generator=None):
        """
        Initialize the GeminiRAGAgent with optional retriever and generator.
        retriever: an object responsible for fetching relevant documents
        generator: an object responsible for generating responses
        """
        self.retriever = retriever
        self.generator = generator

    def retrieve(self, query):
        """
        Retrieve relevant documents given a query.
        """
        if not self.retriever:
            raise ValueError("Retriever not set")
        return self.retriever.retrieve(query)

    def generate(self, context):
        """
        Generate a response given some context.
        """
        if not self.generator:
            raise ValueError("Generator not set")
        return self.generator.generate(context)

    def answer(self, query):
        """
        High-level method to answer a query by retrieving and generating.
        """
        docs = self.retrieve(query)
        context = self._combine_docs(docs)
        response = self.generate(context)
        return response

    def _combine_docs(self, docs):
        """
        Combine retrieved documents into a single context string.
        """
        return "\n".join(docs) if docs else ""

