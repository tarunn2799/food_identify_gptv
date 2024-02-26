import streamlit as st
import os
from llama_index.core import SimpleDirectoryReader
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

# Function to call API and get the response
def get_response(api_key, image_path, prompt):
    os.environ["OPENAI_API_TOKEN"] = api_key
    image_documents = SimpleDirectoryReader(input_files=[image_path]).load_data()

    openai_mm_llm = OpenAIMultiModal(
        model="gpt-4-vision-preview", api_key=api_key, max_new_tokens=300
    )
    response = openai_mm_llm.complete(
        prompt=prompt,
        image_documents=image_documents,
    )
    return response.text

# Streamlit app starts here
st.title("Image Analysis App")

st.session_state['api_key'] = st.secrets['OPENAI_KEY']

# Input for OpenAI API Key
# api_key_placeholder = st.empty()
# api_key_input = api_key_placeholder.text_input("Enter your OPENAI API Key", type="password", key="api_input")

if st.button("Set API Key") or 'api_key' in st.session_state:
    if api_key_input:
        st.session_state['api_key'] = api_key_input
        api_key_placeholder.empty()  # Remove the input box after setting the API key
        st.success("API Key is set. You can now upload images.")

        # Image Upload
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            # Save the uploaded image to use in the API call
            with open("uploaded_image.jpeg", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

            # Prompt Modification
            default_prompt = "The image contains a food item. You are required to look at it and tell me what food product it is. If the image is anything other than a food product, reply 'Not a food product'. Describe what you're seeing in the image in 1 sentence maximum."
            prompt = st.text_area("Modify the prompt if needed:", value=default_prompt, height=150)

            # Process image with API on button click
            if st.button('Analyze Image'):
                response = get_response(st.session_state['api_key'], "uploaded_image.jpeg", prompt)
                st.write(response)
