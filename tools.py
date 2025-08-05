from flask import Flask, request, jsonify
import cohere

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