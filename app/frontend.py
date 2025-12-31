# frontend.py
import streamlit as st
import requests

st.set_page_config(page_title="Insurance Predictor", page_icon=":bar_chart:")
st.title("Insurance Charge Predictor")

api_url = st.text_input("API URL", value="http://127.0.0.1:8000/predict")

with st.form(key="input_form"):
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    bmi = st.number_input("BMI", min_value=10.0, max_value=80.0, value=25.0, format="%.1f")
    children = st.number_input("Number of children", min_value=0, max_value=10, value=0)
    smoker = st.selectbox("Smoker?", ["No", "Yes"])
    smoker_encoded = 1 if smoker == "Yes" else 0
    submit = st.form_submit_button("Predict")

if submit:
    payload = {"age": int(age), "bmi": float(bmi), "children": int(children), "smoker_encoded": int(smoker_encoded)}
    try:
        with st.spinner("Sending request to backend..."):
            resp = requests.post(api_url, json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        if "prediction" in result:
            st.success(f"Prediction: {result['prediction']}")
            st.json(result)
        else:
            st.error("No 'prediction' field found in response.")
            st.write(result)
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        st.write("Make sure the FastAPI server is running and the API URL is correct.")
