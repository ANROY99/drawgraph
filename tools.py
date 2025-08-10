from flask import Flask, request, jsonify
import requests
import cohere
import http.client
import json
import pandas as pd
import openpyxl
from openpyxl import Workbook
import base64

def get_base_prompt(file_path):
    
    """Read the base prompt from a local file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""  # Return empty string if no base prompt file is found
    except Exception as e:
        raise Exception(f"Error reading base prompt file: {str(e)}")



def check_intent(input_text,p_api_key):

    # Path to the local file containing the base prompt (optional)
    BASE_PROMPT_FILE_PATH = 'prompt_01.txt'
    output_text = ''

    base_prompt = get_base_prompt(BASE_PROMPT_FILE_PATH)
    final_prompt = f"{base_prompt}\n{output_text}" if base_prompt else output_text
    final_prompt = final_prompt + '. The user query is as follows :'+input_text
    co = cohere.ClientV2(api_key=p_api_key)
    
    # Use output_text as the prompt for Cohere API
    response = co.chat(
        model="command-a-03-2025",
        messages=[
                   {
                     "role": "user",
                     "content": final_prompt
                   }
                 ]
    )

    generated_text = response.message.content[0].text.strip()
    return generated_text


def generate_SQL(input_text,p_api_key):

    # Path to the local file containing the base prompt (optional)
    BASE_PROMPT_FILE_PATH = 'prompt_02.txt'
    output_text = ''

    base_prompt = get_base_prompt(BASE_PROMPT_FILE_PATH)
    final_prompt = f"{base_prompt}\n{output_text}" if base_prompt else output_text
    final_prompt = final_prompt + '. The user query is as follows :'+input_text
    co = cohere.ClientV2(api_key=p_api_key)
    
    # Use output_text as the prompt for Cohere API
    response = co.chat(
        model="command-a-03-2025",
        messages=[
                   {
                     "role": "user",
                     "content": final_prompt
                   }
                 ]
    )

    generated_SQL = response.message.content[0].text.strip()
    return generated_SQL


def validate_output(input_text,p_api_key):

    # Path to the local file containing the base prompt (optional)
    BASE_PROMPT_FILE_PATH = 'prompt_03.txt'
    output_text = ''

    base_prompt = get_base_prompt(BASE_PROMPT_FILE_PATH)
    final_prompt = f"{base_prompt}\n{output_text}" if base_prompt else output_text
    final_prompt = final_prompt + '. The user query is as follows :'+input_text
    co = cohere.ClientV2(api_key=p_api_key)
    
    # Use output_text as the prompt for Cohere API
    response = co.chat(
        model="command-a-03-2025",
        messages=[
                   {
                     "role": "user",
                     "content": final_prompt
                   }
                 ]
    )

    validated_output = response.message.content[0].text.strip()
    return validated_output


def sanitize_text(text):
    formatting_chars = ['\n', '\t', '\r', '\b', '\f']
    found_chars = [char for char in formatting_chars if char in text]

    if found_chars:
        print(f"Found formatting characters: {', '.join(repr(c) for c in found_chars)}")
        for char in found_chars:
            text = text.replace(char, ' ')  # Remove each found character
    else:
        print("No formatting characters found.")

    return text


def execute_query(p_in_query):
    conn = http.client.HTTPSConnection("GB55491B372E79A-ANINDYAATP23AI.adb.us-chicago-1.oraclecloudapps.com")
    payload = {"query_string": p_in_query}
    json_payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "/ords/app/rest-v6/user_query/", json_payload, headers)
    res = conn.getresponse()
    data = res.read()
    extracted_data = (data.decode("utf-8"))
    return extracted_data

def generate_excel(p_in_user_session,p_in_result,p_in_sql_text):

    # Parse the string into a Python list of dictionaries
    order_list = json.loads(p_in_result)


    # Convert to a DataFrame
    df = pd.DataFrame(order_list)

    l_filename = "data_"+str(p_in_user_session)+".xlsx"


    # Save to Excel
    #df.to_excel(l_filename,sheet_name='Result', index=False)

    with pd.ExcelWriter(l_filename) as writer:
        df.to_excel(writer, sheet_name="Data", index=False)
        # Put SQL text in a DataFrame so it can be written as a single-column sheet
        pd.DataFrame([p_in_sql_text]).to_excel(writer, sheet_name="SQL", index=False, header=False)

    with open(l_filename, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
    
    UCMDocId = upload_result(encoded_bytes.decode("utf-8"),l_filename)
 
    return UCMDocId


def upload_result(p_in_base64_excel,p_in_filename):

    url = "https://fa-eqju-test-saasfaprod1.fa.ocs.oraclecloud.com/fscmRestApi/resources/11.13.18.05/erpintegrations"

    payload = json.dumps({"OperationName": "uploadFileToUCM","DocumentContent":p_in_base64_excel,"DocumentAccount": "fin$/payables$/import$","ContentType": "xlsx","FileName": p_in_filename,"DocumentId": None})
    headers = {'Content-Type': 'application/json','Authorization': 'Basic YW5pbmR5YS5yQHRjcy5jb206S29sa2F0YUA5OQ=='}

    response = requests.request("POST", url, headers=headers, data=payload)

    json_data = json.loads(response.text)

    document_id = json_data["DocumentId"]

    return (document_id)


