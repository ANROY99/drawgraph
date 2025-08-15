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
import pandas as pd
import openpyxl
from openpyxl import Workbook
import base64
import requests



# Initialize Flask app
app = Flask(__name__)

# Replace with your Cohere API key

COHERE_API_KEY = os.environ.get('api_key')
#COHERE_API_KEY = 'YRHcYuNL9pFZmvIjPlGZE10gDGa2NKjH07GHGXeL'




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
      
        print('Here1')
      
        l_generated_SQL = generate_SQL(input_text,COHERE_API_KEY)
        
        print('Here2')
        
        l_validated_output = sanitize_text(l_generated_SQL)

        print('Here3')

        l_output_data = execute_query(l_validated_output)

        print('Here4')

        l_sanitized_output = sanitize_text(l_output_data)

        print(l_UCMDocId)

        #l_delete_sts = delete_UCMfile(l_UCMDocId)
        l_delete_sts = 'OK'

        l_UCMDocId = generate_excel(user_session,l_sanitized_output,l_validated_output)
        
        

        # Return the result along with the user session and input text
        return jsonify({
            'usersession': user_session,
            'inputtext':input_text,
            'generated_sql': l_validated_output,
            'UCMDocId' : l_UCMDocId,
            'UCMdelSts' : l_delete_sts
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=5000)
     app.run()
