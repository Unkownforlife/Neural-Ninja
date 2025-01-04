from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()


def generate_overview_func(client_requirements):
    try:
        system_prompt = f"""
        Given the following project requirement:
            {client_requirements}

            Generate a detailed project documentation following this structure:

            1. PROJECT OVERVIEW
            Generate based on the requirement:
            - Company Details (extract or infer from requirement)
            - Project Goals (minimum 5 specific goals aligned with the requirement)

            2. KEY FEATURES
            Create relevant sections based on the project type:
            - Essential pages/modules
            - Core functionalities
            - User interfaces
            - System integrations
            - Additional features
            All sections should be detailed with bullet points.

            3. TECHNICAL STACK
            Recommend appropriate:
            - Frontend technologies
            - Backend technologies
            - Database solutions
            - Hosting & Deployment options
            - Additional tools and integrations

            4. TIMELINE AND MILESTONES
            Create a phase-wise breakdown table:
            [Phase | Tasks | Duration]

            5. BUDGET ESTIMATE
            Generate a realistic budget table:
            [Category | Estimated Cost (USD)]

            6. METRICS FOR SUCCESS
            List 6-7 measurable success metrics relevant to the project type.

            7. FUTURE SCALABILITY
            List 3-4 potential future enhancements.

            8. RISK MANAGEMENT
            Create a risk assessment table: 
            [Risk | Mitigation Plan]

            9. TEAM ROLES
            Create a roles and responsibilities table:
            [Role | Responsibilities]

            10. CONCLUSION
            Summarize the project's strategic importance.

            Format all sections using markdown with clear hierarchical headers (###) and maintain consistent formatting with bullet points (-) and tables where specified.
        """

        message = [{"role": "system", "content": system_prompt}]

        response = llm.chat(model="gpt-4-1106-preview", messages=message)

        # md_path = "result.md"
        
        # with open(md_path, "w") as file:
        #     file.write(response)

        return response

    except Exception as e:
        return {"status": "error", "message": "Uh oh!!! Server is down"}, 500

if __name__ == "__main__":
    client_requirements = "Consider you are a project manager, I want to develop a website for my company NeuralNinjas.com, Which is working in emerging tech and blockchain development. We provide services for these. We  have 40 people team and existing. on last 5 years. Can you create project analysis document"
    client_requirements = "Create a hr automation project"
    # prd_document_generation(client_requirements)
