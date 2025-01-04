from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

import json
from loguru import logger
from llms import OpenAILLM
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request


###--------------------------------------------------------------------------###


llm = OpenAILLM()


###--------------------------------------------------------------------------###


def landing_page(payload):
    required_params = ["client_requirement"]
    if any(param not in payload for param in required_params):
        return create_response(False, "Required parameters missing", {}, 400)

    try:
        client_requirements = payload.get("client_requirement")

        system_prompt = f"""

        Here Initial Requirements : {client_requirements}

        You are a creative and detail-oriented assistant skilled in generating website prompts tailored to professional and industry-specific needs. When tasked with creating a prompt for a personal portfolio, your output should:

        Reflect the individual’s expertise and career focus.
        Include specific core features for showcasing skills, experience, and projects effectively.
        Suggest a modern and professional UI/UX style tailored to their field of expertise.
        Ensure the prompt balances professionalism, creativity, and technical appeal.

        Always maintain clarity and conciseness, ensuring the prompt can be easily understood and actionable by a designer or developer.

        ** I need final prompt 10 to 13 lines only**

        ** When you generate the prompt conside above prompt as example and every use way prompt generation **

        ** Basic Example Prompt **
        Develop a professional website for NeuralNinjas.com, an established company specializing in emerging tech and blockchain development services. The website should showcase the company's 5-year history, highlight their expertise in cutting-edge technologies, and present their service offerings. It should also reflect the scale of their 40-person team and their industry presence.
        Core features:
        Home page introducing the company and its core services
        Detailed service pages for emerging tech and blockchain development
        Team showcase highlighting key members
        Case studies or project portfolio
        Contact form for potential clients
        UI/Style:
        Futuristic and sleek design with subtle blockchain-inspired elements
        Dynamic animations to represent emerging technologies
        Color scheme balancing professionalism with innovation: deep blues, electric greens, and metallic accents
        """
        message = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        result = llm.chat(
            model="gpt-4-1106-preview",
            messages=message,
            max_response_tokens=700,
            temperature=0.3,
        )

        return create_response(
            True, "Landing Page prompt generated successfully", result, 200
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        return create_response(False, f"Error: {str(e)}", {}, 500)


###--------------------------------------------------------------------------###


def create_response(status, message, data, code):
    """Creates a response object with status, message, data, and HTTP status code."""
    return {"status": status, "message": message, "data": data}, code
