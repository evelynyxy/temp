import streamlit as st
import pandas as pd
import base64
import requests
from io import StringIO


st.title("Read CSV from GitHub")

url = "https://raw.githubusercontent.com/evelynyxy/temp/main/data.csv"

def load_data():
    return pd.read_csv(url)

try:
    df = load_data()
    st.success("Data loaded successfully!")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load data: {e}")



">> https://github.com/settings/personal-access-tokens "
a = st.text_input("Enter a")
b = st.text_input("Enter b")
c = st.text_input("Enter c")

if st.button("Upload to GitHub"):
    # Your new data
    new_data = pd.DataFrame([{"a": a, "b": b, "c": c}])

    url = "https://api.github.com/repos/evelynyxy/temp/contents/data2.csv"
    headers = {"Authorization": f"token {st.secrets['github']['token']}"}

    # Try to get existing file
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = r.json()
        sha = content["sha"]
        old_csv = base64.b64decode(content["content"]).decode()
        old_data = pd.read_csv(StringIO(old_csv))
        combined = pd.concat([old_data, new_data], ignore_index=True)
    else:
        sha = None
        combined = new_data

    # Prepare payload
    csv = combined.to_csv(index=False)
    payload = {
        "message": "Update data2.csv",
        "content": base64.b64encode(csv.encode()).decode(),
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    st.success("Uploaded!") if r.status_code in [200, 201] else st.error("Upload failed.")
    
