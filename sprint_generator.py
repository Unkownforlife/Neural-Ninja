from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()


def generate_sprint(client_requirements):
    print(f"{client_requirements = }")
    try:
        system_prompt = f"""
        You are a sprint planning expert and agile coach. Your task is to generate a detailed sprint plan based on client requirements. The sprint plan should include:  
            1. **Project Objective**: A summary of the project's main goal.  
            2. **Sprint Goals**: Clearly defined goals for the sprint.  
            3. **Sprint Timeline**: A timeline for the sprint (e.g., 2 weeks, 4 weeks).  
            4. **Backlog Items**: A breakdown of requirements into actionable backlog items, with priority levels.  
            5. **Roles and Responsibilities**: Assignment of roles and tasks to team members (e.g., developers, designers, testers, etc.).  
            6. **Deliverables**: Key deliverables expected at the end of the sprint.  
            7. **Risks and Mitigation**: Identification of potential risks and suggestions for mitigation.  
            8. **Tools and Technologies**: Recommended tools and technologies for successful completion.  
            9. **Definition of Done (DoD)**: Criteria for considering the sprint successful.  

        Be concise yet comprehensive while structuring the plan. Use a professional and practical approach to ensure the sprint is feasible.
        """

        message = [{
            "role": "system", 
            "content": system_prompt
            },
            {
                "role": "user",
                "content": client_requirements
        }]

        response = llm.chat(model="gpt-4-1106-preview", messages=message)

        # md_path = "sprint.md"

        # with open(md_path, "w") as file:
        #     file.write(response)
        print(response)

        return response

    except Exception as e:
        return {"status": "error", "message": "Uh oh!!! Server is down"}, 500

if __name__ == "__main__":
    client_requirements = "Consider you are a project manager, I want to develop a website for my company NeuralNinjas.com, Which is working in emerging tech and blockchain development. We provide services for these. We  have 40 people team and existing. on last 5 years. Can you create project analysis document"
    client_requirements = "Create a hr automation project"
    generate_sprint(client_requirements)
    
