import streamlit as st
import pandas as pd
import base64
import requests


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
    # Step 1: Load existing data from GitHub
    try:
        existing_df = pd.read_csv(raw_url)
    except:
        existing_df = pd.DataFrame(columns=["a", "b", "c"])  # If file doesn't exist yet

    # Step 2: Append new row
    new_row = pd.DataFrame([{"a": a, "b": b, "c": c}])
    updated_df = pd.concat([existing_df, new_row], ignore_index=True)

    # Step 3: Convert to CSV and encode in base64
    csv_content = updated_df.to_csv(index=False)
    content_encoded = base64.b64encode(csv_content.encode()).decode()

    # Step 4: Get SHA of existing file (required by GitHub API)
    headers = {"Authorization": f"token {st.secrets['github']['token']}"}
    sha = None
    get_resp = requests.get(github_api_url, headers=headers)
    if get_resp.status_code == 200:
        sha = get_resp.json()["sha"]

    # Step 5: Upload updated file to GitHub
    payload = {
        "message": "Append new row to data2.csv",
        "content": content_encoded,
        "branch": "main",
        "sha": sha  # Required to update existing file
    }

    put_resp = requests.put(github_api_url, headers=headers, json=payload)

    if put_resp.status_code in [200, 201]:
        st.success("Data appended to GitHub successfully!")
    else:
        st.error(f"Failed to upload. Status: {put_resp.status_code}, Message: {put_resp.text}")

