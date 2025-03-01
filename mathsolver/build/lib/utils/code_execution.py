import io
import sys
import contextlib

def execute_python_code(code):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            exec(code)
            return output.getvalue().strip()
        except Exception as e:
            return f"Error: {str(e)}"