from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()


def prd_document_generation():

    with open("result.md", 'r', encoding='utf-8') as file:
            content = file.read()

    system_prompt = f"""
        Create a detailed Product Requirements Document (PRD) for [PROJECT_NAME] using the following structure:

        1. INTRODUCTION
        Detail the following:
        - Purpose
        - Goals (list 3-4 specific goals)
        - Target Audience (bullet points of primary user groups)

        2. FUNCTIONAL REQUIREMENTS
        2.1 [PRODUCT/SYSTEM] Features
        Detail each major section/module with bullet points including:
        - Key features
        - Functionality details
        - Sub-features where applicable

        2.2 Technical Features
        List all technical requirements including:
        - Platform requirements
        - Integration needs
        - Security features
        - Future scalability considerations

        3. NON-FUNCTIONAL REQUIREMENTS
        List specific requirements for:
        - Performance
        - Reliability
        - Usability
        - Accessibility
        - Maintainability

        4. USER STORIES
        Break down for each user type:
        - As a [user type]:
        - List 2-3 specific user stories

        5. DESIGN REQUIREMENTS
        Detail:
        - Visual Design (theme, colors, typography)
        - UI/UX Requirements

        6. TECHNICAL STACK
        Specify:
        - Frontend technologies
        - Backend technologies
        - Database
        - Hosting
        - Additional tools

        7. PROJECT TIMELINE
        Create a phase-wise table:
        [Phase | Deliverables | Duration]

        8. RISKS AND MITIGATION
        Create a table with:
        [Risk | Impact | Mitigation Strategy]

        9. ACCEPTANCE CRITERIA
        List 5-6 specific criteria for project completion

        10. APPENDIX
        Include:
        - References
        - Glossary of technical terms

        Format using markdown with clear hierarchical headers (**) and maintain consistent formatting with bullet points (-) and tables where specified.

        Project Requirement:

        {content}
        """

    message = [{"role": "system", "content": system_prompt}]

    response = llm.chat(model="gpt-4-1106-preview", messages=message)

    md_path = "result.md"

    with open(md_path, "w") as file:
        file.write(response)

    return md_path


if __name__ == "__main__":
    
    prd_document_generation()
