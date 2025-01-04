from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()


def generate_closing_doc_func(client_requirements):
    try:
        system_prompt = f"""
        Given the following client requirements:
            {client_requirements}

            Generate a detailed closing document following this structure:

            1. EXECUTIVE SUMMARY
            Provide a brief overview of the project, its goals, and outcomes.

            2. PROJECT ACHIEVEMENTS
            Highlight the key achievements and milestones reached during the project:
            - Major deliverables
            - Key milestones
            - Success stories

            3. CHALLENGES AND SOLUTIONS
            Describe the main challenges faced during the project and the solutions implemented:
            - Challenge 1: Description
              Solution: Description
            - Challenge 2: Description
              Solution: Description

            4. FINAL DELIVERABLES
            List and describe the final deliverables provided to the client:
            - Deliverable 1: Description
            - Deliverable 2: Description

            5. CLIENT FEEDBACK
            Summarize the feedback received from the client:
            - Positive feedback
            - Areas for improvement

            6. LESSONS LEARNED
            Outline the key lessons learned during the project:
            - Lesson 1: Description
            - Lesson 2: Description

            7. FUTURE RECOMMENDATIONS
            Provide recommendations for future projects or next steps:
            - Recommendation 1: Description
            - Recommendation 2: Description

            8. CLOSING REMARKS
            Conclude the document with final thoughts and acknowledgments.

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
