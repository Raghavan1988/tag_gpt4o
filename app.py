import streamlit as st
import openai
from openai import OpenAI
import requests
from io import BytesIO
import base64
import replicate
import json

st.set_page_config(layout="wide")

client = OpenAI()

def translate_to_english(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful translator to English."},
            {"role": "user", "content": "Translate it to English. Other language: " + text + " Strictly output English translation ONLY"}
        ])
    return response.choices[0].message.content

def detect_n_translate(english_response, original_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful language detector."},
            {"role": "user", "content": original_input +" What is the language? Answer should be JUST THE NAME OF THE LANGUAGE in 1 word"}
        ])
    language =  response.choices[0].message.content
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful translator from english to " + language},
            {"role": "user", "content": original_input +"Translate the following english content to the Language: " + language + " English: " + english_response + " output only translated content." }
        ])
    return (language, response.choices[0].message.content)

def generate_image(description):
    english = translate_to_english(description)
    prompt = description + " " + english
    URL = get_replicate_url(prompt)
    return URL

def get_perplexity_response(input):
    question = input
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
    "model": "llama-3-sonar-large-32k-online",
    "messages": [
        {
            "role": "system",
            "content": "Answer accurately"
        },
        {
            "role": "user",
            "content": question
        }
    ]
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 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"
    }
    response = requests.post(url, json=payload, headers=headers)
    responseD = json.loads(response.text)

    return responseD["choices"][0]["message"]["content"]

def get_replicate_url(description):
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "width": 768,
            "height": 768,
            "prompt": description,
            "refine": "expert_ensemble_refiner",
            "scheduler": "K_EULER",
            "lora_scale": 0.6,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "apply_watermark": False,
            "high_noise_frac": 0.8,
            "negative_prompt": "",
            "prompt_strength": 0.8,
            "num_inference_steps": 25
            }
        )
    return output[0]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

st.title("Universal Polyglot")
st.markdown("by Raghavan Muthuregunathan")
st.markdown("- You can ask anything in any language and either generate an image or get an answer")
mode = st.radio("Choose Mode:", ("Image Mode", "Perplexity Search Engine Mode", "Image Input"))

example1 = "(Tamil) இந்தியாவில் நெல் வயலில் விளையாடும் ஒரு சிறுவனும் பெண்ணும்"
example2 = "(Hindi) भारत में शुष्क मौसम के दौरान कौन सी फसलें उगाई जानी चाहिए?"
example3 = "(indonesian) Apa yang terjadi pada bayinya?"
example4 = ""
st.markdown("- " + example1)
st.markdown("- " + example2)
st.markdown("- " + example3)

input_text = st.text_area("Enter the question or describe for image generation (Use any Indian or Middle Eastern Language):")

if mode == "Image Input":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

if st.button("Submit"):
    if mode == "Perplexity Search Engine Mode":
        if input_text:
            translated_text = translate_to_english(input_text)
            english_response = get_perplexity_response(translated_text)
            st.subheader("Response in local language")
            (local_language, local_response) = detect_n_translate(english_response, input_text)
            st.write(local_response)
            st.markdown('<font color="red" size="small">LLMs are known to hallucinate</font>', unsafe_allow_html=True)            
            st.write("\n\n-------\n")
            with st.expander("Debug output"):
                st.write("Input in english:" + translated_text.strip())
                st.write(english_response)
                st.write("---------")
                st.write("detected language :" + local_language)
        else:
            st.error("Please enter some text to translate or describe for image generation.")
    
    elif mode == "Image Mode":
        if input_text:
            image_url = generate_image(input_text)
            if image_url:
                st.subheader("Generated Image:")
                st.image(image_url)
            else:
                st.error("Failed to generate image.")
        else:
            st.error("Please enter some text to translate or describe for image generation.")

    elif mode == "Image Input":
        if uploaded_file and input_text:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": [
                        {"type": "text", "text": input_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
                    ]}
                ]
            )
            st.subheader("Response:")
            st.write(response.choices[0].message.content)
        else:
            st.error("Please upload an image and enter a question.")
