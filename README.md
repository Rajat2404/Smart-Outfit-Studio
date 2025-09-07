# Smart Outfit Studio - Virtual Try-On

Welcome to **Smart Outfit Studio**! This app lets you virtually try on outfits, experiment with fashion, and get AI-powered styling advice.

## Features

- **Virtual Try-On:** Mix and match sample models and garments, or upload your own images.
- **Fashion Assistant:** Ask questions about fashion, styling, or trends and get instant AI advice.
- **Customization:** Adjust garment cropping, denoise level, and random seed for personalized results.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Smart-Outfit-Studio.git
cd Smart-Outfit-Studio
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and replace with your credentials:
```
GEMINI_API_KEY="your gemini api key"
HF_TOKEN="your HF token"
```

### 4. Run the App

```bash
streamlit run app.py
```

## Folder Structure

- `app.py` — Main Streamlit application.
- `example/` — Sample human images.
- `sample_garments/` — Sample garment images.
- `.env.example` — Example environment variable file.

## API Keys

- **Gemini API Key:** Get from [Google AI Studio](https://aistudio.google.com/).
- **Hugging Face Token:** Get from [Hugging Face](https://huggingface.co/settings/tokens).

## Usage

1. Select or upload a human image.
2. Select or upload a garment image.
3. Customize options as desired.
4. Click **Try-On Now** to generate results.
5. Use the **Fashion Assistant** tab for AI-powered advice.

