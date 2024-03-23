CODE_GENERATOR_PROMPT = f"""Task: Develop a method to {{code_prompt}} in {{code_language}} language. Ensure that the method accepts a sample input, executes it, and prints the result.

Guidelines:
1. Design a method that performs {{code_prompt}} functionality in {{code_language}}.
2. Implement the method to accept a sample input as an argument.
3. Execute the method with the sample input.
4. Print the result obtained from the method execution.
5.Make sure the program doesn't ask for any input from the user

Instructions:
- Define a method that performs the specified {{code_prompt}}.
- Ensure the method is capable of accepting various sample inputs.
- Execute the method with a sample input and print the result on the screen.
- Return the properly executable code with proper indentations if applicable and dont return any explanations.
"""


CODE_FIX_PROMPT = f"""
                 Task: Correct the code snippet provided below in the {{code_language}} programming language, following the given instructions.
                 Instructions for Fixing:
                 Initial code prompt :{{code_prompt}}
                 Requested change :   {{fix_guidelines}}
                 Code Language: {{code_language}}

                 Here is the code snippet:
                 ```{{code_snippet}}
                 
                 ```

                 Instructions:
                 1. Identify and rectify any syntax errors, logical issues, or bugs in the code.
                 2. Ensure that the code produces the desired output.
                 3. Comment on each line where you make changes, explaining the nature of the fix.
                 4. Verify that only corrected code is displayed in the output.

                 Please make sure that the fixed code is included in the output, along with comments detailing the modifications made.
                 """
