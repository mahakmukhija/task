from transformers import AutoTokenizer, AutoModelForCausalLM

def load_llama():
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-2-13b-chat-hf",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
    return model, tokenizer

def load_deepseek():
    model = AutoModelForCausalLM.from_pretrained(
        "deepseek-ai/deepseek-llm-13b-chat",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-13b-chat")
    return model, tokenizer
