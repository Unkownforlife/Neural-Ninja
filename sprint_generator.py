from dotenv import load_dotenv, find_dotenv
import json
load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()


def generate_sprint(client_requirements):
    print(f"{client_requirements = }")
    try:
        # system_prompt = f"""
        # You are a sprint planning expert and agile coach. Your task is to generate a detailed sprint plan based on client requirements. The sprint plan should include:  
        #     1. **Project Objective**: A summary of the project's main goal.  
        #     2. **Sprint Goals**: Clearly defined goals for the sprint.  
        #     3. **Sprint Timeline**: A timeline for the sprint (e.g., 2 weeks, 4 weeks).  
        #     4. **Backlog Items**: A breakdown of requirements into actionable backlog items, with priority levels.  
        #     5. **Roles and Responsibilities**: Assignment of roles and tasks to team members (e.g., developers, designers, testers, etc.).  
        #     6. **Deliverables**: Key deliverables expected at the end of the sprint.  
        #     7. **Risks and Mitigation**: Identification of potential risks and suggestions for mitigation.  
        #     8. **Tools and Technologies**: Recommended tools and technologies for successful completion.  
        #     9. **Definition of Done (DoD)**: Criteria for considering the sprint successful.  

        # Be concise yet comprehensive while structuring the plan. Use a professional and practical approach to ensure the sprint is feasible.
        # """

        # message = [{
        #     "role": "system", 
        #     "content": system_prompt
        #     },
        #     {
        #         "role": "user",
        #         "content": client_requirements
        # }]

        system_prompt = """
            You are a sprint planning expert and agile coach. Your task is to generate a sprint plan in **strict JSON format** based on client requirements. 
            The JSON structure must follow this exact schema:

            {
            "project_name": "string",
            "project_objective": "string",
            "sprint_goals": ["string"],
            "sprint_timeline": {
                "duration": "string",
                "start_date": "YYYY-MM-DD",
                "end_date": "YYYY-MM-DD"
            },
            "backlog_items": [
                { "item_name": "string", "priority": "string" }
            ],
            "roles_and_responsibilities": {
                "role_name": ["string"]
            },
            "deliverables": ["string"],
            "risks_and_mitigation": [
                { "risk": "string", "mitigation": "string" }
            ],
            "tools_and_technologies": ["string"],
            "definition_of_done": ["string"]
            }

            ### Rules:
            1. **Only output valid JSON** in the exact structure above. Do not include any additional text outside the JSON.
            2. Use placeholders or realistic sample data if specific information is missing.
            3. Ensure all keys match the schema exactly and are in lowercase.
            4. Always generate valid, well-formed JSON, even if the input is incomplete.

            Respond only with JSON adhering strictly to the schema above.
            """

        user_prompt = f"""
            Generate a sprint plan for the following client requirements:
            
            {client_requirements}
        """

        message = [{
            "role": "system", 
            "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
        }]


        response = llm.chat(model="gpt-4-1106-preview", messages=message)
        json_output = json.loads(response.replace("```json", "").replace("```", "").strip())
        print(json_output)

        return json_output

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": "Uh oh!!! Server is down"}, 500

if __name__ == "__main__":
    client_requirements = "Consider you are a project manager, I want to develop a website for my company NeuralNinjas.com, Which is working in emerging tech and blockchain development. We provide services for these. We  have 40 people team and existing. on last 5 years. Can you create project analysis document"
    client_requirements = "Create a hr automation project"
    print(generate_sprint(client_requirements))
    
