from flask import Flask, request, jsonify
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





@app.route('/generate', methods=['POST'])
def generate_text():
    try:

        l_UCMDocId = 0
        # Get JSON payload from the request
        data = request.get_json()
        user_session = data.get('usersession')
        input_text = data.get('input_text')

        # Validate user session and input text
        if not isinstance(user_session, int):
            return jsonify({'error': 'Invalid or missing "usersession" in payload'}), 400
        if not input_text:
            return jsonify({'error': 'Missing "input_text" in payload'}), 400

        l_intent = check_intent(input_text,COHERE_API_KEY)
      
        print(l_intent)
      
        if l_intent == "**SalesData**":
      
            l_generated_SQL = generate_SQL(input_text,COHERE_API_KEY)
        
            print(l_generated_SQL)
            
            check_graphtype(input_text,l_generated_SQL,COHERE_API_KEY)
        
            l_validated_output = sanitize_text(l_generated_SQL)

            print('Here3')

            l_output_data = execute_query(l_validated_output)

            #print('Here4')

            l_sanitized_output = sanitize_text(l_output_data)

            print(l_sanitized_output)

            #l_delete_sts = delete_UCMfile(l_UCMDocId)
            l_delete_sts = 'OK'

            l_dataURL = generate_excel(user_session,l_sanitized_output,l_validated_output,APPS_BASICAUTH,APPS_USERNAME,APPS_PASSWORD)
        
            l_imageURL = gen_bargraph_script(l_sanitized_output,user_session,COHERE_API_KEY,APPS_BASICAUTH,APPS_USERNAME,APPS_PASSWORD)
            

            # Return the result along with the user session and input text
            return jsonify({
                'usersession': user_session,
                'inputtext':input_text,
                'generated_sql': l_validated_output,
                'DataURL' : l_dataURL,
                'UCMdelSts' : l_delete_sts,
                'ImageURL' : l_imageURL,
                'ResponseText' : ''
            })
        
        elif l_intent == "**BillingData**":
            print("Processing Billingdata...")
        else:
            print("Unknown intent. Please check the value of l_intent.")
            return jsonify({
                'usersession': user_session,
                'inputtext':'At present, the tool can handle only Sales Data or Billing Data related queries' ,
                'generated_sql': '',
                'UCMDocId' : '',
                'UCMdelSts' : ''
            })
            

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=5000)
     app.run()
