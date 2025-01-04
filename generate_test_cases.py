from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()



def generate_test_cases(requirement):
    try:
        system_prompt = """
            You are a highly skilled software tester and QA expert. Your job is to analyze requirements provided by the user and generate detailed test cases. Follow these guidelines:
            - **Output Format:** Strictly format the output in Markdown.
            - **Test Case Structure:** Each test case must include:
            - Test Case ID
            - Test Scenario
            - Test Steps
            - Expected Result
            - **Coverage:** Ensure the test cases cover functional, usability, performance, security, and compatibility aspects where applicable.
            - **Formatting:** Do not include any extra text or explanations outside the Markdown format.
            - **Clarity and Precision:** Ensure test steps and expected results are clear and concise.
            """


            # User prompt (provides the specific requirement)
        user_prompt = f"""
            I have a specific requirement and need detailed test cases for it. Please analyze the following requirement and generate test cases in the specified format:

            **Requirement:** {requirement}
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
        response = response.replace("```markdown", "").replace("```", "").strip()

        md_path = "test_cases.md"

        with open(md_path, "w") as file:
            file.write(response)
        return response

    except Exception as e:
        return {"status": "error", "message": "Uh oh!!! Server is down"}, 500


if __name__ == "__main__":
    client_requirements = "Consider you are a project manager, I want to develop a website for my company NeuralNinjas.com, Which is working in emerging tech and blockchain development. We provide services for these. We  have 40 people team and existing. on last 5 years. Can you create project analysis document"
    client_requirements = "Create a hr automation project"
    generate_test_cases(client_requirements)
