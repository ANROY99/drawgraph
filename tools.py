from flask import Flask, request, jsonify
import requests
import cohere
import http.client
import json
import pandas as pd
import openpyxl
from openpyxl import Workbook
import base64
import xml.etree.ElementTree as ET
from urllib.parse import unquote

l_did = 0


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

def generate_excel(p_in_user_session,p_in_result,p_in_sql_text,p_in_basicauth,p_in_uname,p_in_pwd):

    # Parse the string into a Python list of dictionaries
    order_list = json.loads(p_in_result)


    # Convert to a DataFrame
    df = pd.DataFrame(order_list)

    l_filename = "ORDdata_"+str(p_in_user_session)+".xlsx"


    # Save to Excel
    #df.to_excel(l_filename,sheet_name='Result', index=False)

    with pd.ExcelWriter(l_filename) as writer:
        df.to_excel(writer, sheet_name="Data", index=False)
        # Put SQL text in a DataFrame so it can be written as a single-column sheet
        pd.DataFrame([p_in_sql_text]).to_excel(writer, sheet_name="SQL", index=False, header=False)

    with open(l_filename, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
    
    UCMDocId = upload_result(encoded_bytes.decode("utf-8"),l_filename,p_in_basicauth,p_in_uname,p_in_pwd)

    did = UCMDocId
 
    return UCMDocId


def upload_result(p_in_base64_excel,p_in_filename,p_basic_auth,p_in_uname,p_in_pwd):

    print('Here5')

    l_did = check_UCMfile(p_in_filename,p_in_uname,p_in_pwd)
    
    print('Here6')
    
    print(l_did)
    
    if l_did is not None:
        l_del_response = delete_UCMfile(l_did,p_in_uname,p_in_pwd)
        print(l_del_response)

    url = "https://fa-eqju-test-saasfaprod1.fa.ocs.oraclecloud.com/fscmRestApi/resources/11.13.18.05/erpintegrations"

    payload = json.dumps({"OperationName": "uploadFileToUCM","DocumentContent":p_in_base64_excel,"DocumentAccount": "fin$/payables$/import$","ContentType": "xlsx","FileName": p_in_filename,"DocumentId": None})
    #headers = {'Content-Type': 'application/json','Authorization': 'Basic YW5pbmR5YS5yQHRjcy5jb206S29sa2F0YUA5OQ=='}
    headers = {'Content-Type': 'application/json','Authorization': p_basic_auth}

    response = requests.request("POST", url, headers=headers, data=payload)
    
    json_data = json.loads(response.text)

    document_id = json_data["DocumentId"]
    
    l_url = get_doc_url(document_id,p_in_uname,p_in_pwd)

    return (l_url)


def delete_UCMfile(did,p_in_uname,p_in_pwd):
    
    url = "https://fa-eqju-test-saasfaprod1.fa.ocs.oraclecloud.com/idcws/GenericSoapPort"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    # Construct the SOAP XML payload
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body xmlns:ns1="http://www.oracle.com/UCM">
        <ns1:GenericRequest webKey="cs">
          <ns1:Service IdcService="DELETE_DOC">
            <ns1:User></ns1:User>
            <ns1:Document>
              <ns1:Field name="dID">{did}</ns1:Field>
            </ns1:Document>
          </ns1:Service>
        </ns1:GenericRequest>
      </soap:Body>
    </soap:Envelope>"""

    print(payload)

    # Send the POST request with basic authentication
    response = requests.post(url, data=payload, headers=headers, auth=(p_in_uname, p_in_pwd))

    # Return response status and content
    return {
        "response_text": response.status_code
    }


def check_UCMfile(p_in_filename,p_in_uname,p_in_pwd):

    did = None
    
    url = "https://fa-eqju-test-saasfaprod1.fa.ocs.oraclecloud.com/idcws/GenericSoapPort"
    l_filedID = 0
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    # Construct the SOAP XML payload
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body xmlns:ns1="http://www.oracle.com/UCM">
        <ns1:GenericRequest webKey="cs">
          <ns1:Service IdcService="GET_SEARCH_RESULTS">
            <ns1:User></ns1:User>
            <ns1:Document>
              <ns1:Field name="QueryText">&lt;qsch&gt;{p_in_filename}&lt;/qsch&gt;</ns1:Field>
            </ns1:Document>
          </ns1:Service>
        </ns1:GenericRequest>
      </soap:Body>
    </soap:Envelope>"""

    #print(payload)

    # Send the POST request with basic authentication
    soap_response = requests.post(url, data=payload, headers=headers, auth=(p_in_uname,p_in_pwd))

    soap_message = soap_response.content
    
    xml_content = soap_message.decode('utf-8')
    
    # Remove MIME headers to isolate the XML content
    xml_start = xml_content.find('<env:Envelope')
    
    xml_end = xml_content.find('</env:Envelope>') + len('</env:Envelope>')
    
    xml_content = xml_content[xml_start:xml_end]
    
    #print(xml_content)
    print('Here7')

    root = ET.fromstring(xml_content)
    namespace = {'ns0': 'http://www.oracle.com/UCM', 'env': 'http://schemas.xmlsoap.org/soap/envelope/'}
    
    print('Here8')
    
    total_rows = 0
    
    total_rows_element = root.find('.//ns0:Field[@name="TotalRows"]', namespace)
    
    print('Here9'+total_rows_element.text)
    
    total_rows = int(total_rows_element.text)
    print('Total Rows : '+str(total_rows))
        
    
    
        
    if (total_rows > 0):
        
        # Extract dID (assuming it's in a ResultSet)
        did = None
        did_element = root.find('.//ns0:Field[@name="dID"]', namespace)
        if did_element is not None:
            did = did_element.text
    

    print(str(did))

    # Return response status and content
    return did

def get_doc_url(p_in_did,p_in_uname,p_in_pwd):
    # SOAP API endpoint
    url = "https://fa-eqju-test-saasfaprod1.fa.ocs.oraclecloud.com/idcws/GenericSoapPort"
    
    # SOAP request payload template
    payload_template = """
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body xmlns:ns1="http://www.oracle.com/UCM">
            <ns1:GenericRequest webKey="cs">
                <ns1:Service IdcService="DOC_INFO">
                    <ns1:User></ns1:User>
                    <ns1:Document><ns1:Field name="dID">{did}</ns1:Field></ns1:Document>
                </ns1:Service>
            </ns1:GenericRequest>
        </soap:Body>
    </soap:Envelope>
    """
    
    # Replace {did} with the input parameter
    payload = payload_template.format(did=p_in_did)
    
    #print(payload)
    
    # Headers for SOAP request
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    
    try:
        # Send SOAP request
        soap_response = requests.post(url, data=payload, headers=headers, auth=(p_in_uname,p_in_pwd))
        print('Here13')
                
        soap_message = soap_response.content
    
        xml_content = soap_message.decode('utf-8')
    
        # Remove MIME headers to isolate the XML content
        xml_start = xml_content.find('<env:Envelope')
    
        xml_end = xml_content.find('</env:Envelope>') + len('</env:Envelope>')
    
        xml_content = xml_content[xml_start:xml_end]
    
        #print(xml_content)
        print('Here7')
         
        soap_response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the XML response
        root = ET.fromstring(xml_content)
        
        # Find the DocUrl field in the response
        doc_url = root.find(".//ns0:Field[@name='DocUrl']", namespaces={"ns0": "http://www.oracle.com/UCM"})
        
        if doc_url is not None:
            decoded_url = unquote(doc_url.text)
            new_prefix = 'https://fa-eqju-test-saasfaprod1.fa.ocs.oraclecloud.com'
            common_path_start = decoded_url.find('/cs/groups/fafusionimportexport/')
            if common_path_start != -1:
                decoded_url = new_prefix + decoded_url[common_path_start:]
            decoded_url = decoded_url.replace('~1.xlsx', '.xlsx')
            return decoded_url
        else:
            return None
        
    except requests.RequestException as e:
        print(f"Error invoking SOAP API: {e}")
        return None
