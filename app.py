from flask import Flask, request, jsonify, Response
import cohere
import os
from tools import get_base_prompt
from tools import check_intent
from tools import generate_SQL
from tools import validate_output
from tools import sanitize_text
from tools import execute_query
from tools import generate_excel
from tools import delete_UCMfile
from tools import get_doc_url
from tools import check_graphtype
from tools import gen_bargraph_script
from tools import gen_linechart_script
from tools import get_ERP_data
import pandas as pd
import openpyxl
from openpyxl import Workbook
import base64
import requests



# Initialize Flask app
app = Flask(__name__)

# Replace with your Cohere API key

COHERE_API_KEY = os.environ.get('api_key')
APPS_USERNAME = os.environ.get('apps_uname')
APPS_PASSWORD = os.environ.get('apps_pwd')
APPS_BASICAUTH = os.environ.get('basic_auth')
APPS_PODURL = os.environ.get('pod_url')

l_imageURL = ''



@app.route('/generate', methods=['POST'])
def generate_text():
    try:

        l_UCMDocId = 0
        l_img_b64 = ''
        l_tables = ''
        # Get JSON payload from the request
        data = request.get_json()
        user_session = data.get('usersession')
        input_text = data.get('input_text')

        # Validate user session and input text
        if not isinstance(user_session, int):
            return jsonify({'error': 'Invalid or missing "usersession" in payload'}), 400
        if not input_text:
            return jsonify({'error': 'Missing "input_text" in payload'}), 400



      
        l_generated_SQL = input_text
        
            
        l_output_data = get_ERP_data(l_generated_SQL,APPS_USERNAME,APPS_PASSWORD,APPS_PODURL)

        print('Here4')

        l_sanitized_output = sanitize_text(l_output_data)
            
        print('Here5')

        print(l_sanitized_output)


        # Return the result along with the user session and input text
        return jsonify({
            'usersession': user_session,
            'inputtext':input_text,
            'ResponseText' : l_sanitized_output
        })


 

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
        



if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=5000)
     app.run()


