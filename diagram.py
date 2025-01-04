import re
import requests
import json


def extract_executive_summary(markdown_content):
    # Pattern to match the section from ### 1.1 Executive Summary until the next heading
    pattern = r'### 1\.1 Executive Summary\n(.*?)(?=\n###|\Z)'
    
    # Search for the pattern in the content using regex with DOTALL flag to match newlines
    match = re.search(pattern, markdown_content, re.DOTALL)
    
    if match:
        # Get the content and strip whitespace
        summary = match.group(1).strip()
        return summary
    else:
        return "Executive Summary section not found"


def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"
    

def send_summary_post(summary, api_url):
    try:
        # Prepare the payload
        payload = {
            "media_id": 5245,
            "problem_statement":summary
        }
        
        # Set headers for JSON content
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:            
            response = requests.post(api_url, 
                                data=json.dumps(payload), 
                                headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request: {str(e)}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {str(e)}")


def update_system_architecture(markdown_content, image_url):
    # Pattern to find the System Architecture section
    arch_pattern = r'(### 4\.1 System Architecture\n)(.*?)(?=\n###|\Z)'
    
    match = re.search(arch_pattern, markdown_content, re.DOTALL)
    if not match:
        raise ValueError("System Architecture section not found")
    
    # Get the existing content and add image
    section_header = match.group(1)
    section_content = match.group(2).strip()
    
    # Create updated content with image
    updated_content = f"{section_header}{section_content}\n\n![System Architecture]({image_url})\n"
    
    # Replace the old section with updated content
    new_markdown = re.sub(arch_pattern, updated_content, markdown_content, flags=re.DOTALL)
    print(new_markdown)
    return new_markdown


# Example usage
if __name__ == "__main__":
    # Read the markdown file
    markdown_file = 'result.md'
    content = read_markdown_file(markdown_file)
    
    # Extract the executive summary
    summary = extract_executive_summary(content)

    API_URL = "https://xkdz2q6z2tjfcllbaltakt76m40yseiu.lambda-url.us-east-1.on.aws/"
    response_data = send_summary_post(summary, API_URL)
    image_url = response_data.get('URL')
    updated_content = update_system_architecture(content, image_url)

    with open(markdown_file, 'w', encoding='utf-8') as file:
            file.write(updated_content)
    
    # Print the result
    print("Executive Summary:")
    print("-----------------")
    print(summary)