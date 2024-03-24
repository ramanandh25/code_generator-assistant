
from langchain.llms import Ollama, CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from .log_utils import CodeGenLogger
import subprocess
import tempfile
import os
from .config import CODE_GENERATOR_PROMPT, CODE_FIX_PROMPT
import re


llm = Ollama(model="codellama:7b")


def clean_response_to_code(response: str) -> str:
    try:
        # Regular expression to match code blocks
        code_blocks = re.findall(r"```([\s\S]*?)```", response)

        # If there are no code blocks, return the original response
        if not code_blocks:
            CodeGenLogger.lgr.info("No code blocks found in the response.")
            return response.strip()

        # If there is more than one code block, return all of them
        if len(code_blocks) > 1:
            CodeGenLogger.lgr.info(
                f"Found {len(code_blocks)} code blocks in the response."
            )
            return "\n\n".join(code_blocks).strip()

        # If there is only one code block, return it
        extracted_code = code_blocks[0].strip()
        CodeGenLogger.lgr.info(
            f"Extracted the code {extracted_code} from the generated response {response}."
        )
        return extracted_code
    except Exception as e:
        CodeGenLogger.lgr.error(
            f"Error {e} occurred while cleaning code from response."
        )
        raise ValueError("Error occurred while cleaning code from response.")


def generate_code(code_prompt: str, code_language: str) -> str:
    try:
        # Log information about the code generation process
        CodeGenLogger.lgr.info(
            f"Generating code for the prompt: '{code_prompt}' in language: '{code_language}'"
        )

        # Define code_template and memory
        memory = ConversationBufferMemory(
            input_key="code_prompt", memory_key="chat_history"
        )

        template = CODE_GENERATOR_PROMPT

        # Prompt Templates
        code_template = PromptTemplate(
            input_variables=["code_prompt", "code_language"], template=template
        )
        code_chain = LLMChain(
            llm=llm,
            prompt=code_template,
            output_key="code",
            memory=memory,
            verbose=True,
        )
        generated_code = code_chain.invoke(
            {"code_prompt": code_prompt, "code_language": code_language}
        )
        CodeGenLogger.lgr.info(
            f"Generated the code {generated_code['code']} for prompt {code_prompt}"
        )
        return generated_code["code"]

    except Exception as e:
        # Log the error
        CodeGenLogger.lgr.error(
            f"An error occurred during code generation: {e} for prompt {code_prompt}"
        )

        # Return an error message
        return f"Error occurred during code generation: {e}"


def fix_generated_code(
    code_snippet: str, fix_guidelines: str, code_language: str, code_prompt: str
) -> str:
    try:
        # Assuming you have a memory to store the conversation
        memory = ConversationBufferMemory(
            input_key="code_prompt", memory_key="chat_history"
        )

        # Improved instructions template
        template = CODE_FIX_PROMPT

        # LLM Chains definition
        # Create a chain that fixes the code
        fix_generated_template = PromptTemplate(
            input_variables=[
                "code_prompt",
                "code_language",
                "code_snippet",
                "fix_guidelines",
            ],
            template=template,
        )

        fix_generated_chain = LLMChain(
            llm=llm,
            prompt=fix_generated_template,
            output_key="fixed_code",
            memory=memory,
            verbose=True,
        )
        # Prepare the input for the chain
        input_data = {
            "code_prompt": code_prompt,
            "code_language": code_language,
            "code_snippet": code_snippet,
            "fix_guidelines": fix_guidelines,
        }

        # Run the chain
        output = fix_generated_chain.invoke(input_data)

        # Log success
        CodeGenLogger.lgr.info(
            f"Code snippet fixed successfully: {output['fixed_code']}"
        )
        CodeGenLogger.lgr.info(f"Code fix instructions: {fix_guidelines}")

        return output["fixed_code"]

    except Exception as e:
        # Log error
        CodeGenLogger.lgr.error(f"Error occurred while fixing code snippet: {e}")
        # Raise or return an appropriate error message
        raise ValueError("Error occurred while fixing code snippet")


def log_error(message: str):
    CodeGenLogger.lgr.error(message)


def execute_python_code(code: str) -> str:
    # Create a temporary directory to work in
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary file to save the code
        temp_file_path = os.path.join(temp_dir, "temp_code.py")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(code)

        # Run the Python script
        run_result = subprocess.run(
            ["python", temp_file_path],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Ensure output is text, not bytes
        )

        # Check for errors
        if run_result.returncode != 0:
            error_message = run_result.stderr
            CodeGenLogger.lgr.error(
                f"Errr occured while executing python code {error_message}"
            )
            return f"Error occurred while executing Python code: {error_message}"

        CodeGenLogger.lgr.info(
            f"Executed python code for {code} and got {run_result.stdout} output"
        )
        # Return the execution result
        return run_result.stdout


def execute_code(code: str, language: str) -> str:
    try:
        code = clean_response_to_code(code)
        # Validate the language
        if language not in ["python", "java", "c++"]:
            raise ValueError(f"Unsupported language for execution: {language}")

        # Log the execution attempt
        CodeGenLogger.lgr.info(f"Attempting to execute {language} code.")

        if language == "python":
            # Execute Python code
            return execute_python_code(code)
        elif language == "java":
            # Execute Java code
            return "Execution not implemented for java"
        elif language == "c++":
            # Execute C++ code
            return "Execution not implemented for c++"

    except ValueError as ve:
        CodeGenLogger.lgr.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        error_message = str(e)
        CodeGenLogger.lgr.error(
            f"Unexpected error occurred while executing code: {error_message}"
        )
        raise ValueError(f"Unexpected error occurred: {error_message}")
