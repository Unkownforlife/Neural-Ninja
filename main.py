from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from llms import OpenAILLM


llm = OpenAILLM()


def prd_document_generation(client_requirements):

    system_prompt = f"""
    You are a Senior Project Manager with experince with 10 year. Client Requirements : {client_requirements} Create a detailed Project Analysis Document (PAD) for the client requirements:

    Document Structure Requirements:
    1. Create a professional, well-structured document with clear sections and subsections
    2. Use markdown formatting for better readability
    3. Include section numbers
    4. Maintain consistent formatting throughout
    5. Include detailed tables where relevant

    Required Document Sections:
    1. Product Overview
    - Executive Summary
    - Problem Statement
    - Business Objectives

    2. Requirements & Specifications
    - Functional Requirements 
    - Non- Functional Features
    - Performance Requirements
    - Security Requirements

    3. Feature Specifications
    - Feature Description
    - Priority Level
    - Dependencies
    - Constraints
    - Success Metrics

    4. Design & Architecture
    - System Architecture
    - Data Models
    - API Specifications
    - Integration Requirements

    5. Timeline & Milestones
    - Development Phases
    - Release Schedule
    - Key Deliverables
    - Dependencies
    ** Important ** :
            Required Timeline Structure:

            1. Development Phases Overview
            - Include 4 main phases (Discovery & Planning, Design & Development, Testing & Optimization, Deployment & Launch)
            - Break down into 2-week sprints


            2. Sprint Details for Each Phase
            For each sprint, provide:
            - Sprint number and timeframe
            - Main objectives
            - Detailed tasks with subtasks (minimum 5 subtasks per task)
            - Clear deliverables
            - Dependencies

            3. Key Deliverables Section
            For each phase, list:
            - Required deliverables
            - Acceptance criteria
            - Dependencies
            - Stakeholder sign-offs needed

            4. Dependencies Mapping
            Include:
            - Critical path dependencies
            - External dependencies
            - Inter-sprint dependencies
            - Resource dependencies

            5. Milestone Schedule
            Create a table with:
            - Milestone ID
            - Deliverable description
            - Timeline (Week number)
            - Dependencies
            - Status tracking

            6. Risk Factors & Contingencies
            Detail:
            - Timeline risks and buffers
            - Technical risk mitigation
            - Resource risk management
            - External dependency management

            Formatting Requirements:
            1. Use proper markdown headers (# for main sections, ## for subsections)
            2. Include checkboxes for all tasks: [ ]
            3. Use tables for milestone schedules
            4. Use consistent indentation for hierarchy
            5. Include clear section breaks

            ## 5.1 Development Phases Overview

                ### Phase 1: Discovery & Planning (Weeks 1-2)
                - Sprint 1 (Weeks 1-2)
                - [ ] Requirements Gathering
                    - [ ] Stakeholder interviews
                    - [ ] Current system analysis
                    - [ ] User research sessions
                    - [ ] Pain points documentation
                    - [ ] Requirements prioritization
                - [ ] Technical Assessment
                    - [ ] System architecture review
                    - [ ] Technology stack evaluation
                    - [ ] Integration points analysis
                    - [ ] Performance requirements definition
                    - [ ] Security requirements assessment

                ### Phase 2: Design & Development (Weeks 3-8)
                - Sprint 2 (Weeks 3-4)
                - [ ] System Design
                    - [ ] Architecture blueprint creation
                    - [ ] Database schema design
                    - [ ] API endpoints definition
                    - [ ] Security framework design
                    - [ ] Integration patterns documentation
                - [ ] UI/UX Design
                    - [ ] Wireframe creation
                    - [ ] User flow mapping
                    - [ ] Design system setup
                    - [ ] Prototype development
                    - [ ] Accessibility compliance check

                - Sprint 3 (Weeks 5-6)
                - [ ] Core Development
                    - [ ] Database implementation
                    - [ ] Basic CRUD operations
                    - [ ] Authentication system
                    - [ ] Core API development
                    - [ ] Error handling framework
                - [ ] Frontend Development
                    - [ ] Component library setup
                    - [ ] Core pages development
                    - [ ] State management implementation
                    - [ ] API integration
                    - [ ] Unit test setup

                - Sprint 4 (Weeks 7-8)
                - [ ] Feature Development
                    - [ ] Advanced functionality implementation
                    - [ ] Integration with external services
                    - [ ] Performance optimization
                    - [ ] Security implementation
                    - [ ] Documentation
                - [ ] Quality Assurance
                    - [ ] Test case creation
                    - [ ] Unit testing
                    - [ ] Integration testing
                    - [ ] Performance testing
                    - [ ] Security testing

                ### Phase 3: Testing & Optimization (Weeks 9-10)
                - Sprint 5 (Weeks 9-10)
                - [ ] System Testing
                    - [ ] End-to-end testing
                    - [ ] User acceptance testing
                    - [ ] Load testing
                    - [ ] Security audit
                    - [ ] Bug fixing
                - [ ] Performance Optimization
                    - [ ] Code optimization
                    - [ ] Database optimization
                    - [ ] Caching implementation
                    - [ ] Load balancing setup
                    - [ ] Monitoring setup

                ### Phase 4: Deployment & Launch (Weeks 11-12)
                - Sprint 6 (Weeks 11-12)
                - [ ] Pre-deployment
                    - [ ] Environment setup
                    - [ ] Configuration management
                    - [ ] Data migration
                    - [ ] Backup system setup
                    - [ ] Rollback plan creation
                - [ ] Launch
                    - [ ] Production deployment
                    - [ ] Health monitoring
                    - [ ] Performance monitoring
                    - [ ] User support setup
                    - [ ] Documentation handover


            Note: Ensure all timelines are realistic and include buffer time for unexpected delays. Each sprint should have clear, measurable objectives and deliverables.

    6. Success Metrics & Analytics
    - KPIs
    - Success Criteria
    - Measurement Methods

    7. Assumptions & Constraints
    - Business Constraints
    - Technical Constraints
    - Resource Constraints
    - Timeline Constraints

    8. Risks & Mitigation Strategies
    - Identified Risks
    - Impact Assessment
    - Mitigation Plans

    Output Format:
    Generate the document in markdown format with proper formatting, spacing, and section breaks.

    Note: The generated document should be comprehensive, professional, and ready for stakeholder review.
    """

    message = [{"role": "system", "content": system_prompt}]

    response = llm.chat(model="gpt-4-1106-preview", messages=message)

    md_path = "result.md"

    with open(md_path, "w") as file:
        file.write(response)

    return md_path


if __name__ == "__main__":
    client_requirements = "Consider you are a project manager, I want to develop a website for my company NeuralNinjas.com, Which is working in emerging tech and blockchain development. We provide services for these. We  have 40 people team and existing. on last 5 years. Can you create project analysis document"
    prd_document_generation(client_requirements)
