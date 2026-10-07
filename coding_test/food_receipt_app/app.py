import streamlit as st
import os
import tempfile
from coding_test.food_receipt_app.extractor import extract_receipt
from coding_test.food_receipt_app.database import insert_receipt
from coding_test.food_receipt_app.agent import answer_user_query

st.set_page_config(page_title="AI Receipt Tracker", layout="wide")
st.title("AI Food Receipt Tracker")

with st.sidebar:
    st.header("1. Upload Receipt")
    uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Receipt Preview", use_container_width=True)
        
        if st.button("Extract & Save to DB", type="primary"):
            with st.spinner("AI is extracting data..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    extracted_data = extract_receipt(tmp_file_path)
                    receipt_id = insert_receipt(extracted_data)
                    
                    if receipt_id:
                        st.success(f"Success! Saved to DB with ID: {receipt_id}")
                        with st.expander("View Extracted JSON"):
                            st.json(extracted_data)
                    else:
                        st.error("Failed to save to database.")
                        
                except Exception as e:
                    st.error(f"Error processing receipt: {e}")
                finally:
                    os.unlink(tmp_file_path)

st.header("2. Ask About Your Expenses")
st.markdown("Try asking: *'What food did I buy yesterday?'* or *'Where did I buy hamburger from last 7 day'*")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your receipts..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Querying database..."):
            response = answer_user_query(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})