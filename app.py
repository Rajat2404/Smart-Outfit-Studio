import os
import tempfile
from dotenv import load_dotenv
import streamlit as st
from gradio_client import Client, file
import google.generativeai as genai

load_dotenv() 
# Configure Gemini API
genai.configure(api_key=os.getenv("api_key"))


# Streamlit page setup (must be first Streamlit command)
st.set_page_config(page_title="Virtual Try-On Studio", layout="wide")


def get_gemini_response(question):
    """Interact with Gemini chatbot for fashion advice."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Hugging Face token and Gradio client initialization
hf_token = os.getenv("HF_TOKEN")
vton_client = Client("yisol/IDM-VTON", hf_token=hf_token)

def get_image_dict(folder):
    """Return dictionary of image filenames and their paths."""
    return {img: os.path.join(folder, img) for img in os.listdir(folder) if img.lower().endswith(('.jpg', '.jpeg', '.png'))}

# Directories for sample images
human_dir = "example"
garment_dir = "sample_garments"
human_samples = get_image_dict(human_dir)
garment_samples = get_image_dict(garment_dir)

# --- Streamlit Interface ---
st.title("🧑‍💼👗 Virtual Try-On Studio by RAJAT")
st.markdown("Try different outfits on sample models or upload your own images. Get fashion tips from our AI assistant!")

tabs = st.tabs(["Try-On", "Fashion Assistant"])

with tabs[1]:
    st.header("Fashion Chatbot")
    user_question = st.text_input("Ask about fashion, styling, or trends:")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = ""
    if st.button("Get Advice"):
        answer = get_gemini_response(user_question)
        st.session_state["chat_history"] += f"You: {user_question}\nBot: {answer}\n\n"
    st.text_area("Chat History", st.session_state["chat_history"], height=200)

with tabs[0]:
    st.header("Virtual Try-On")
    left, right = st.columns(2)

    with left:
        st.subheader("Select or Upload Human Image")
        sample_human = st.selectbox("Sample Models:", list(human_samples.keys()))
        st.image(human_samples[sample_human], caption="Selected Model", use_column_width=True)
        uploaded_human = st.file_uploader("Upload your own model image", type=["png", "jpg", "jpeg"], key="human_upload")

    with right:
        st.subheader("Select or Upload Garment")
        sample_garment = st.selectbox("Sample Garments:", list(garment_samples.keys()))
        st.image(garment_samples[sample_garment], caption="Selected Garment", use_column_width=True)
        uploaded_garment = st.file_uploader("Upload your own garment image", type=["png", "jpg", "jpeg"], key="garment_upload")
        garment_desc = st.text_input("Garment Description", value="Stylish outfit")

    st.markdown("---")
    st.subheader("Customization")
    opt1, opt2 = st.columns(2)
    with opt1:
        enable_feature = st.checkbox("Enable Feature", value=True)
        crop_feature = st.checkbox("Crop Garment", value=False)
    with opt2:
        denoise_val = st.slider("Denoise Level", 0, 50, 30)
        seed_val = st.number_input("Random Seed", min_value=0, value=42)

    def save_image_temp(uploaded_file):
        """Save uploaded image to temp directory and return path."""
        if uploaded_file:
            temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return temp_path
        return None

    if st.button("Try-On Now"):
        human_img_path = save_image_temp(uploaded_human) if uploaded_human else human_samples[sample_human]
        garment_img_path = save_image_temp(uploaded_garment) if uploaded_garment else garment_samples[sample_garment]

        if human_img_path and garment_img_path:
            with st.spinner("Generating your try-on result..."):
                try:
                    result = vton_client.predict(
                        dict={
                            "background": file(human_img_path),
                            "layers": [],
                            "composite": None
                        },
                        garm_img=file(garment_img_path),
                        garment_des=garment_desc,
                        is_checked=enable_feature,
                        is_checked_crop=crop_feature,
                        denoise_steps=denoise_val,
                        seed=seed_val,
                        api_name="/tryon"
                    )
                    st.image(result[0], caption="Virtual Try-On Result", use_column_width=True)
                    st.image(result[1], caption="Masked Output", use_column_width=True)
                except Exception as e:
                    st.error(f"Error generating try-on: {e}")
        else:
            st.warning("Please select or upload both a model and a garment image.")