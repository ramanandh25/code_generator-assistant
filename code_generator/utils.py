from .log_utils import CodeGenLogger
from .codellama import generate_code as generate_code_function
from .codellama import fix_generated_code as fix_generated_code_function
from .codellama import execute_code
from fastapi import HTTPException
import re


def clean_response_to_code(response: str) -> str:
    try:
        # Regular expression to match code blocks
        code_blocks = re.findall(r'```([\s\S]*?)```', response)

        # If there are no code blocks, return the original response
        if not code_blocks:
            CodeGenLogger.lgr.info("No code blocks found in the response.")
            return response.strip()

        # If there is more than one code block, return all of them
        if len(code_blocks) > 1:
            CodeGenLogger.lgr.info(f"Found {len(code_blocks)} code blocks in the response.")
            return "\n\n".join(code_blocks).strip()

        # If there is only one code block, return it
        extracted_code = code_blocks[0].strip()
        CodeGenLogger.lgr.info(f"Extracted the code {extracted_code} from the generated response {response}.")
        return extracted_code
    except Exception as e:
        CodeGenLogger.lgr.error(f"Error {e} occurred while cleaning code from response.")
        raise ValueError("Error occurred while cleaning code from response.")


# Example usage:
# response_with_code = "Some text here\n```\nprint('Hello, World!')\n```\nMore text here"
# print(clean_response_to_code(response_with_code))


class CodeManager:
    def __init__(self):
        self.code_prompt = ""
        self.language = ""
        self.generated_code = ""

    def generate_code(self, code_description, lang):
        try:
            self.code_prompt = code_description
            self.language = lang
            self.generated_code = generate_code_function(
                code_prompt=self.code_prompt, code_language=self.language
            )
            return clean_response_to_code(self.generated_code)
        except Exception as e:
            CodeGenLogger.lgr.error(f"Error occurred while generating code: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def fix_code(self, fix_instructions):
        try:
            if not self.generated_code:
                return "No code has been generated yet."
            self.generated_code = fix_generated_code_function(
                fix_guidelines=fix_instructions,
                code_prompt=self.code_prompt,
                code_language=self.language,
                code_snippet=self.generated_code,
            )
            return clean_response_to_code(self.generated_code)
        except Exception as e:
            CodeGenLogger.lgr.error(f"Error occurred while fixing code: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def execute_generated_code(self):
        try:
            if not self.generated_code:
                return "No code has been generated or fixed yet."
            execution_result = execute_code(self.generated_code, self.language)
            return execution_result
        except Exception as e:
            CodeGenLogger.lgr.error(f"Error occurred while executing code: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
