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
import sys
import subprocess
import matplotlib
import xmltodict

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
    
def check_graphtype(input_text,p_in_sql,p_api_key):
    BASE_PROMPT_FILE_PATH = 'prompt_04.txt'
    output_text = ''
    base_prompt = get_base_prompt(BASE_PROMPT_FILE_PATH)
    final_prompt = f"{base_prompt}\n{output_text}" if base_prompt else output_text
    final_prompt = final_prompt + '\n The user query is as follows :'+input_text
    final_prompt = f"{final_prompt}\n{output_text}"+'The SQL statement provided is as follows :\n'+p_in_sql

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
    
    print(generated_text)
        
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
    l_tables = generated_SQL.split('~', 1)[1]
    generated_SQL = generated_SQL.split('~')[0]
    

    return generated_SQL,l_tables


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

def generate_excel(p_in_user_session,p_in_result,p_in_sql_text,p_in_basicauth,p_in_uname,p_in_pwd,p_in_podurl):

    UCMDocId = ''
    print("Here5a")
    
    # Check if p_in_result is empty or None
    if not p_in_result:
        print("p_in_result is empty ot None")
        order_list = []  # Empty list to create an empty DataFrame
    else:
        # Parse the string into a Python list of dictionaries
        parsed_data = json.loads(p_in_result)
        order_list = [parsed_data] if isinstance(parsed_data, dict) else parsed_data
        print("Here5b")

    # If order_list is None (which shouldn't happen with the above check), set it to an empty list
    if order_list is None:
        print("Here5c")
        order_list = []

    # Convert to a DataFrame
    print("Here5d")
    print(order_list)
    df = pd.DataFrame(order_list)

    l_filename = "ORDdata_" + str(p_in_user_session) + ".xlsx"

    # Save to Excel
    with pd.ExcelWriter(l_filename) as writer:
        print("Here5e")
        # If the DataFrame is empty, ensure it has the correct columns
        if df.empty and p_in_result:
            print("Here5f")
            # Extract column names from the first dictionary in the list (if available)
            sample_dict = order_list[0] if order_list else {}
            print("Here5g")
            df = pd.DataFrame(columns=sample_dict.keys())
            print("Here5h")
        df.to_excel(writer, sheet_name="Data", index=False)
        print("Here5i")
        
        # Put SQL text in a DataFrame so it can be written as a single-column sheet
        print("Here5j")
        pd.DataFrame([p_in_sql_text]).to_excel(writer, sheet_name="SQL", index=False, header=False)
        print("Here5k")

    with open(l_filename, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
    
    UCMDocId = upload_result(encoded_bytes.decode("utf-8"), l_filename, p_in_basicauth, p_in_uname, p_in_pwd,p_in_podurl)

    return UCMDocId


def upload_result(p_in_base64_excel,p_in_filename,p_basic_auth,p_in_uname,p_in_pwd,p_in_podurl):

    #print('Here5')

    l_did = check_UCMfile(p_in_filename,p_in_uname,p_in_pwd,p_in_podurl)
    
    #print('Here6')
    
    #print(l_did)
    
    if l_did is not None:
        l_del_response = delete_UCMfile(l_did,p_in_uname,p_in_pwd,p_in_podurl)
        print(l_del_response)

    url = p_in_podurl+"/fscmRestApi/resources/11.13.18.05/erpintegrations"

    payload = json.dumps({"OperationName": "uploadFileToUCM","DocumentContent":p_in_base64_excel,"DocumentAccount": "fin$/payables$/import$","ContentType": "xlsx","FileName": p_in_filename,"DocumentId": None})
    #headers = {'Content-Type': 'application/json','Authorization': 'Basic YW5pbmR5YS5yQHRjcy5jb206S29sa2F0YUA5OQ=='}
    headers = {'Content-Type': 'application/json','Authorization': p_basic_auth}

    response = requests.request("POST", url, headers=headers, data=payload)
    
    json_data = json.loads(response.text)

    document_id = json_data["DocumentId"]
    
    l_url = get_doc_url(document_id,p_in_uname,p_in_pwd,p_in_podurl)

    return (l_url)



def delete_UCMfile(did,p_in_uname,p_in_pwd,p_in_podurl):
    
    url = p_in_podurl+"/idcws/GenericSoapPort"
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

    #print(payload)

    # Send the POST request with basic authentication
    response = requests.post(url, data=payload, headers=headers, auth=(p_in_uname, p_in_pwd))

    # Return response status and content
    return {
        "response_text": response.status_code
    }


def check_UCMfile(p_in_filename,p_in_uname,p_in_pwd,p_in_podurl):

    did = None
    
    url = p_in_podurl+"/idcws/GenericSoapPort"
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
    #print('Here7')

    root = ET.fromstring(xml_content)
    namespace = {'ns0': 'http://www.oracle.com/UCM', 'env': 'http://schemas.xmlsoap.org/soap/envelope/'}
    
    #print('Here8')
    
    total_rows = 0
    
    total_rows_element = root.find('.//ns0:Field[@name="TotalRows"]', namespace)
    
    #print('Here9'+total_rows_element.text)
    
    total_rows = int(total_rows_element.text)
    #print('Total Rows : '+str(total_rows))
        
    
    
        
    if (total_rows > 0):
        
        # Extract dID (assuming it's in a ResultSet)
        did = None
        did_element = root.find('.//ns0:Field[@name="dID"]', namespace)
        if did_element is not None:
            did = did_element.text
    

    #print(str(did))

    # Return response status and content
    return did

def get_doc_url(p_in_did,p_in_uname,p_in_pwd,p_in_podurl):
    # SOAP API endpoint
    url = p_in_podurl+"/idcws/GenericSoapPort"
    
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
        #print('Here7')
         
        soap_response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the XML response
        root = ET.fromstring(xml_content)
        
        # Find the DocUrl field in the response
        doc_url = root.find(".//ns0:Field[@name='DocUrl']", namespaces={"ns0": "http://www.oracle.com/UCM"})
        
        if doc_url is not None:
            decoded_url = unquote(doc_url.text)
            new_prefix = p_in_podurl
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
        
        
def gen_bargraph_script(p_in_result,p_in_user_session,p_api_key,p_basic_auth,p_in_uname,p_in_pwd,p_in_podurl):

    # Path to the local file containing the base prompt (optional)
    BASE_PROMPT_FILE_PATH = 'prompt_05.txt'
    output_text = ''
    UCMurl = ''


    base_prompt = get_base_prompt(BASE_PROMPT_FILE_PATH)
    final_prompt = f"{base_prompt}\n{output_text}" if base_prompt else output_text
    final_prompt = final_prompt + '. The data is as follows :'+p_in_result
    final_prompt = final_prompt + '.\n The file name should be as follows :'+'ORDI'+str(p_in_user_session)+'.jpg'
    print(final_prompt)
    
    l_imagefile = 'ORDI'+str(p_in_user_session)+'.jpg'
    
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
    
    print(generated_text)
    
    l_scriptfile = 'ORDS'+str(p_in_user_session)+'.py'
    
    
    
    with open(l_scriptfile, 'w') as file:
        file.write(generated_text)
    
    python_executable = sys.executable
    subprocess.run([python_executable, l_scriptfile])
    
    with open(l_imagefile, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
    
    UCMurl = upload_result(encoded_bytes.decode("utf-8"),l_imagefile,p_basic_auth,p_in_uname,p_in_pwd,p_in_podurl)
    
    UCMurl = UCMurl.replace('~1.jpg', '.jpg')
    
    print(UCMurl)
    
    return (UCMurl)


def gen_linechart_script(p_in_userquery,p_in_result,p_in_user_session,p_api_key,p_basic_auth,p_in_uname,p_in_pwd):

    # Path to the local file containing the base prompt (optional)
    BASE_PROMPT_FILE_PATH = 'prompt_06.txt'
    output_text = ''
    UCMurl = ''


    base_prompt = get_base_prompt(BASE_PROMPT_FILE_PATH)
    final_prompt = f"{base_prompt}\n{output_text}" if base_prompt else output_text
    final_prompt = final_prompt + '. The data is as follows :'+p_in_result
    final_prompt = final_prompt + '.\n Question based on which this data has been retrieved: '+p_in_userquery
    final_prompt = final_prompt + '.\n The file name should be as follows :'+'ORDI'+str(p_in_user_session)+'.jpg'
    print(final_prompt)
    
    l_imagefile = 'ORDI'+str(p_in_user_session)+'.jpg'
    
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
    
    print(generated_text)
    
    l_scriptfile = 'ORDS'+str(p_in_user_session)+'.py'
    
    
    
    with open(l_scriptfile, 'w') as file:
        file.write(generated_text)
    
    python_executable = sys.executable
    subprocess.run([python_executable, l_scriptfile])
    
    with open(l_imagefile, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
    
    UCMurl = upload_result(encoded_bytes.decode("utf-8"),l_imagefile,p_basic_auth,p_in_uname,p_in_pwd,p_in_podurl)
    
    UCMurl = UCMurl.replace('~1.jpg', '.jpg')
    
    print(UCMurl)
    
    return (UCMurl)
    
def get_ERP_data(p_in_gen_qry,p_in_uname,p_in_pwd,p_in_podurl):
    
    """Read the base query from a local file."""
    
    l_sql_query = p_in_gen_qry
    
    l_query_bytes = l_sql_query.encode('utf-8')
    
    l_base64_query = base64.b64encode(l_query_bytes)
    
    # The following statement is only for printing
    
    l_base64_query_str = l_base64_query.decode('utf-8')
    
    print("Here 4a")
    print(p_in_podurl)
    
    # SOAP API endpoint
    url = p_in_podurl+"/xmlpserver/services/v2/ReportService"
    
    payload_template = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://xmlns.oracle.com/oxp/service/v2">
                      <soapenv:Header>
                      </soapenv:Header>
                         <soapenv:Body>
                            <v2:runReport>
                              <v2:reportRequest>
                                  <v2:attributeFormat>xml</v2:attributeFormat>
                                  <v2:parameterNameValues>
                                     <v2:listOfParamNameValues>
                                       <!--Zero or more repetitions:-->
                                        <v2:item>
                                          <v2:name>query1</v2:name>
                                          <v2:values>
                                             <v2:item>{b64_qry}</v2:item>
                                          </v2:values>
                                       </v2:item>
                                     </v2:listOfParamNameValues>
                                  </v2:parameterNameValues>
                                 <v2:reportAbsolutePath>/Custom/CRYSTLS/SQL_INJ_REP.xdo</v2:reportAbsolutePath>
                                 <v2:reportRawData/>
                                 <v2:sizeOfDataChunkDownload>-1</v2:sizeOfDataChunkDownload>
                             </v2:reportRequest>
                             <v2:userID>{uid}</v2:userID>
                             <v2:password>{pwd}</v2:password>
                           </v2:runReport>
                         </soapenv:Body>
                       </soapenv:Envelope>
    """
    
    payload = payload_template.format(b64_qry=l_base64_query_str,uid=p_in_uname,pwd=p_in_pwd)
    
    #print(payload)
    
    # Headers for SOAP request
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    
    
    try:
        # Send SOAP request
        soap_response = requests.post(url, data=payload, headers=headers, auth=(p_in_uname,p_in_pwd))
        

        response_str = (soap_response.content).decode()

        
        start_pos = response_str.find('<reportBytes>')
        end_pos = response_str.find('</reportBytes>')
        
        response_msg = response_str[start_pos+13:end_pos]
        l_b64_bytes = base64.b64decode(response_msg)

        
        data_start_pos = (l_b64_bytes.decode()).find('<ROW>')
        data_end_pos = (l_b64_bytes.decode()).find('</ROWSET>')
        
 
        xml_data = l_b64_bytes[data_start_pos:data_end_pos].decode()
        
        
        xml_data = '<ROOT>'+xml_data+'</ROOT>'
        
        
        # Parse XML to dictionary
        data_dict = xmltodict.parse(xml_data)
        
        
        # Convert dictionary to JSON
        json_data = json.dumps(data_dict, indent=4)
        
        data = json.loads(json_data)
        
     
        flat_list = []
        if data.get("ROOT") is not None and "ROW" in data["ROOT"]:
           flat_list = data["ROOT"]["ROW"]
        
        result_json = json.dumps(flat_list, indent=4)
             
        
        
        #print(result_json)
        
    
    except requests.RequestException as e:
        print(f"Error invoking SOAP API: {e}")
        return None
    
    return(result_json)
    
    
        
     
def get_ERP_data_final(p_in_gen_qry,p_in_uname,p_in_pwd,p_in_podurl):
    
    """Read the base query from a local file."""
    
    l_sql_query = p_in_gen_qry
    
    BASE_PROMPT_FILE_PATH = 'ORDER_DATA.sql'
    l_ORDER_DATA_sql = get_base_prompt(BASE_PROMPT_FILE_PATH)
    
    l_sql_query = l_sql_query.replace("ORDER_DATA",l_ORDER_DATA_sql)
    
    BASE_PROMPT_FILE_PATH = 'ACTIVE_HOLD_DATA.sql'
    l_ACTIVE_HOLD_DATA_sql = get_base_prompt(BASE_PROMPT_FILE_PATH)
    l_sql_query = l_sql_query.replace("ACTIVE_HOLD_DATA",l_ACTIVE_HOLD_DATA_sql)
    
    BASE_PROMPT_FILE_PATH = 'ONLINE_ORDER_ORCH_DATA.sql'
    l_ONLINE_ORDER_ORCH_DATA_sql = get_base_prompt(BASE_PROMPT_FILE_PATH)
    l_sql_query = l_sql_query.replace("ONLINE_ORDER_ORCH_DATA",l_ONLINE_ORDER_ORCH_DATA_sql)    
    
    print(l_sql_query)
    
    l_query_bytes = l_sql_query.encode('utf-8')
    
    l_base64_query = base64.b64encode(l_query_bytes)
    
    # The following statement is only for printing
    
    l_base64_query_str = l_base64_query.decode('utf-8')
    
    print("Here 4a")
    print(p_in_podurl)
    
    # SOAP API endpoint
    url = p_in_podurl+"/xmlpserver/services/v2/ReportService"
    
    payload_template = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://xmlns.oracle.com/oxp/service/v2">
                      <soapenv:Header>
                      </soapenv:Header>
                         <soapenv:Body>
                            <v2:runReport>
                              <v2:reportRequest>
                                  <v2:attributeFormat>xml</v2:attributeFormat>
                                  <v2:parameterNameValues>
                                     <v2:listOfParamNameValues>
                                       <!--Zero or more repetitions:-->
                                        <v2:item>
                                          <v2:name>query1</v2:name>
                                          <v2:values>
                                             <v2:item>{b64_qry}</v2:item>
                                          </v2:values>
                                       </v2:item>
                                     </v2:listOfParamNameValues>
                                  </v2:parameterNameValues>
                                 <v2:reportAbsolutePath>/Custom/CRYSTLS/SQL_INJ_REP.xdo</v2:reportAbsolutePath>
                                 <v2:reportRawData/>
                                 <v2:sizeOfDataChunkDownload>-1</v2:sizeOfDataChunkDownload>
                             </v2:reportRequest>
                             <v2:userID>{uid}</v2:userID>
                             <v2:password>{pwd}</v2:password>
                           </v2:runReport>
                         </soapenv:Body>
                       </soapenv:Envelope>
    """
    
    payload = payload_template.format(b64_qry=l_base64_query_str,uid=p_in_uname,pwd=p_in_pwd)
    
    print(payload)
    
    # Headers for SOAP request
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    
    
    try:
        # Send SOAP request
        soap_response = requests.post(url, data=payload, headers=headers, auth=(p_in_uname,p_in_pwd))
        

        response_str = (soap_response.content).decode()

        print(response_str)
        
        start_pos = response_str.find('<reportBytes>')
        end_pos = response_str.find('</reportBytes>')
        
        response_msg = response_str[start_pos+13:end_pos]
        l_b64_bytes = base64.b64decode(response_msg)

        
        data_start_pos = (l_b64_bytes.decode()).find('<ROW>')
        data_end_pos = (l_b64_bytes.decode()).find('</ROWSET>')
        
 
        xml_data = l_b64_bytes[data_start_pos:data_end_pos].decode()
        
        
        xml_data = '<ROOT>'+xml_data+'</ROOT>'
        
        
        # Parse XML to dictionary
        data_dict = xmltodict.parse(xml_data)
        
        
        # Convert dictionary to JSON
        json_data = json.dumps(data_dict, indent=4)
        
        data = json.loads(json_data)
        
     
        flat_list = []
        if data.get("ROOT") is not None and "ROW" in data["ROOT"]:
           flat_list = data["ROOT"]["ROW"]
        
        result_json = json.dumps(flat_list, indent=4)
             
        
        
        #print(result_json)
        
    
    except requests.RequestException as e:
        print(f"Error invoking SOAP API: {e}")
        return None
    
    return(result_json)
    
    
        
     