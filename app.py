import streamlit as st
from load_models import load_llama, load_deepseek
from evaluation import evaluate_response
import torch

st.set_page_config(page_title="LLM Topic Understanding Comparison", layout="wide")

st.title("🧠 LLaMA vs DeepSeek: Topic Understanding Evaluation")

prompt = st.text_area("Enter a topic-based prompt", "Explain the impact of AI on modern education systems.")

if st.button("Generate & Compare"):

    with st.spinner("Loading models..."):
        llama_model, llama_tokenizer = load_llama()
        deepseek_model, deepseek_tokenizer = load_deepseek()

    def generate(model, tokenizer, prompt):
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
        outputs = model.generate(**inputs, max_new_tokens=300)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    llama_response = generate(llama_model, llama_tokenizer, prompt)
    deepseek_response = generate(deepseek_model, deepseek_tokenizer, prompt)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🦙 LLaMA Response")
        st.write(llama_response)
        llama_score = evaluate_response(llama_response)
        st.markdown(f"**Accuracy:** {llama_score[0]}  \n**Depth:** {llama_score[1]}  \n**Clarity:** {llama_score[2]}")

    with col2:
        st.subheader("🔍 DeepSeek Response")
        st.write(deepseek_response)
        deepseek_score = evaluate_response(deepseek_response)
        st.markdown(f"**Accuracy:** {deepseek_score[0]}  \n**Depth:** {deepseek_score[1]}  \n**Clarity:** {deepseek_score[2]}")

    st.markdown("---")

    winner = "LLaMA" if sum(llama_score) > sum(deepseek_score) else "DeepSeek" if sum(deepseek_score) > sum(llama_score) else "Tie"
    st.success(f"🏆 **Better Topic Handler:** {winner}")
