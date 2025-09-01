import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

st.set_page_config(page_title="Arabic OCR Search", page_icon="📚")

st.title("📚 Google Books Style OCR Search")
st.markdown("🔎 Upload a PDF or Image and search for Arabic keywords.")

# Upload file
uploaded_file = st.file_uploader(
    "📂 Upload PDF or Image (PDF, PNG, JPG, JPEG)",
    type=["pdf","png","jpg","jpeg"]
)

if uploaded_file:
    file_type = uploaded_file.type
    st.success(f"✅ File uploaded successfully! ({uploaded_file.name})")
    
    # Get keyword input
    keyword = st.text_input("🔎 Enter keyword to search", "")
    
    if keyword:
        with st.spinner('🔎 Searching...'):
            text = ""
            
            try:
                # PDF
                if file_type == "application/pdf":
                    pages = convert_from_bytes(uploaded_file.read(), dpi=300)
                    for page in pages:
                        text += pytesseract.image_to_string(page, lang='ara')
                
                # Image
                else:
                    image = Image.open(uploaded_file)
                    text = pytesseract.image_to_string(image, lang='ara')
            
            except Exception as e:
                st.error(f"⚠️ Error processing file: {e}")
            
            # Show results
            if keyword in text:
                st.success(f"✅ Keyword '{keyword}' FOUND in document!")
            else:
                st.warning(f"❌ Keyword '{keyword}' NOT found in document.")
