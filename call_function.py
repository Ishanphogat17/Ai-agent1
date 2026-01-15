from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)

# Map function names to actual function implementations
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call, verbose=False):
    """
    Execute a function call from the LLM and return the result.
    
    Args:
        function_call: A types.FunctionCall object with name and args properties
        verbose: If True, print detailed function call information
        
    Returns:
        A types.Content object with the function result or error
    """
    # Get function name, ensuring it's a string
    function_name = function_call.name or ""
    
    # Print function call info
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    # Check if function exists in our map
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Make a copy of the arguments and set working directory
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    
    # Call the function with the arguments
    function_result = function_map[function_name](**args)
    
    # Return the result wrapped in a types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    ) 
