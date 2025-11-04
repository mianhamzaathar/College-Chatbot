from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class DeepSeek:
    def __init__(self):
        self.model_name = "deepseek-ai/deepseek-llm-7b"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
    
    def load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16
        ).to(self.device)
    
    def generate(self, prompt: str) -> str:
        if not self.model:
            self.load_model()
            
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=150)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)