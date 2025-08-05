from flask import Flask, request, jsonify
import cohere
from tools import get_base_prompt
from tools import check_intent
from tools import generate_SQL
from tools import validate_output
from tools import sanitize_text


# Initialize Flask app
app = Flask(__name__)

# Replace with your Cohere API key
COHERE_API_KEY = 'YRHcYuNL9pFZmvIjPlGZE10gDGa2NKjH07GHGXeL'


@app.route('/generate', methods=['POST'])
def generate_text():
    try:
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
      
        l_generated_SQL = generate_SQL(input_text,COHERE_API_KEY)
        
        l_validated_output = sanitize_text(l_generated_SQL)

        # Return the result along with the user session and input text
        return jsonify({
            'usersession': user_session,
            'inputtext':input_text,
            'generated_text': l_validated_output
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=5000)
     app.run()
