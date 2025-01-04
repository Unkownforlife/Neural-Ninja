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


{'project_name': 'HR Automation Project', 'project_objective': 'To automate various HR processes to improve efficiency and accuracy', 'sprint_goals': ['Design a user-friendly employee self-service portal', 'Automate the leave application process', 'Implement an automated system for tracking employee hours'], 'sprint_timeline': {'duration': '2 weeks', 'start_date': '2023-04-10', 'end_date': '2023-04-24'}, 'backlog_items': [{'item_name': 'Employee self-service portal UI design', 'priority': 'High'}, {'item_name': 'Leave application process automation', 'priority': 'High'}, {'item_name': 'Employee hours tracking system', 'priority': 'Medium'}, {'item_name': 'Integration testing', 'priority': 'Low'}], 'roles_and_responsibilities': {'Project Manager': ['Oversee project execution', 'Resource allocation', 'Stakeholder communication'], 'UI/UX Designer': ['Create portal design mockups', 'Ensure user experience quality'], 'Software Developer': ['Develop automation features', 'Write unit tests'], 'QA Engineer': ['Conduct testing', 'Report bugs and issues']}, 'deliverables': ['Completed designs for the employee self-service portal', 'Working prototype of the leave application automation', 'First version of the employee hours tracking system'], 'risks_and_mitigation': [{'risk': 'Delays in UI design approval', 'mitigation': 'Early stakeholder engagement and regular updates'}, {'risk': 'Technical challenges in automation', 'mitigation': 'Allocate time for research and proof of concept'}, {'risk': 'Resource unavailability', 'mitigation': 'Cross-training team members to handle multiple roles'}], 'tools_and_technologies': ['Figma for UI/UX design', 'JavaScript and Node.js for backend development', 'React for frontend development', 'JIRA for project management', 'Selenium for automated testing'], 'definition_of_done': ['Designs reviewed and approved by stakeholders', 'Code is written, reviewed, and merged to the main branch', 'All unit tests are passing', 'Feature is tested and accepted by QA']}