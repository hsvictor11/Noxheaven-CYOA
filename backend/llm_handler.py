from llama_cpp import Llama

class LocalLLM:
    def __init__(self):
        self.llm = Llama(
            model_path="./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",  # Update this path
            n_ctx=2048,  # Context window size
            n_threads=4  # Adjust based on your CPU cores
        )

    def generate(self, prompt):
        output = self.llm(
            prompt,
            max_tokens=200,  # Limit response length
            stop=["</end>"],  # Stop generation at this token
            temperature=0.7,  # Creativity vs. determinism
            echo=False  # Don't return the input prompt
        )
        return output["choices"][0]["text"].strip()