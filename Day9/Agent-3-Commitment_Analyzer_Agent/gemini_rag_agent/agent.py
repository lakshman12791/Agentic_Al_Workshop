# # gemini_rag_agent/agent.py

# class SimpleRetriever:
#     def __init__(self, documents):
#         self.documents = documents

#     def retrieve(self, query):
#         # Simple keyword-based retrieval (for demo purposes)
#         return [doc for doc in self.documents if any(word in doc.lower() for word in query.lower().split())]

# class SimpleGenerator:
#     def generate(self, context):
#         # Dummy generator — in real use, you'd connect this to Gemini API
#         return f"Based on the following context:\n\n{context}\n\n...here's a synthesized answer."

# class GeminiRAGAgent:
#     def __init__(self, documents=None, retriever=None, generator=None):
#         """
#         Initialize the GeminiRAGAgent with optional retriever, generator, or raw documents.
#         If documents are provided, a default retriever is created.
#         """
#         if documents and retriever is None:
#             retriever = SimpleRetriever(documents)
#         if generator is None:
#             generator = SimpleGenerator()

#         self.retriever = retriever
#         self.generator = generator

#     def retrieve(self, query):
#         if not self.retriever:
#             raise ValueError("Retriever not set")
#         return self.retriever.retrieve(query)

#     def generate(self, context):
#         if not self.generator:
#             raise ValueError("Generator not set")
#         return self.generator.generate(context)

#     def answer(self, query):
#         docs = self.retrieve(query)
#         context = self._combine_docs(docs)
#         response = self.generate(context)
#         return response

#     def _combine_docs(self, docs):
#         return "\n".join(docs) if docs else ""

#     def query(self, query):
#         return self.answer(query)

# gemini_rag_agent/agent.py

import google.generativeai as genai

class GeminiRAGAgent:
    def __init__(self, model_name="models/gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def analyze(self, lifestyle, startup_idea):
        prompt = (
            "You are a startup mentor. Analyze the founder's current lifestyle and the scope of their startup idea.\n\n"
            f"**Lifestyle**: {lifestyle}\n"
            f"**Startup Idea**: {startup_idea}\n\n"
            "Give realistic feedback on their commitment ability and timeline feasibility."
        )

        response = self.model.generate_content(prompt)
        return response.text
