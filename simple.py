import sys
import time
import uuid
import traceback
from io import StringIO
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import json

@dataclass
class ExecutionResult:
    execution_id: str
    code: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time_seconds: float = 0.0

def execute_unique_code(code_str: str, custom_globals: Optional[Dict[str, Any]] = None) -> ExecutionResult:
    """
    Executes a block of Python code dynamically with a unique execution ID.
    Captures stdout, stderr, execution duration, and potential exceptions.
    """
    execution_id = str(uuid.uuid4())
    
    # Setup namespaces for safety and scoping
    if custom_globals is None:
        custom_globals = {}
    
    # Ensure standard built-ins are available
    if "__builtins__" not in custom_globals:
        custom_globals["__builtins__"] = __builtins__
        
    custom_locals: Dict[str, Any] = {}
    
    # Redirect stdout and stderr to capture print statements and error tracebacks
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    captured_io = StringIO()
    sys.stdout = captured_io
    sys.stderr = captured_io
    
    start_time = time.perf_counter()
    success = True
    error_msg = None
    
    try:
        # Compile and execute the code
        compiled_code = compile(code_str, f"<unique-execution-{execution_id}>", "exec")
        exec(compiled_code, custom_globals, custom_locals)
    except Exception:
        success = False
        # Capture full traceback
        error_msg = traceback.format_exc()
    finally:
        end_time = time.perf_counter()
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
    execution_time = end_time - start_time
    output_str = captured_io.getvalue()
    
    return ExecutionResult(
        execution_id=execution_id,
        code=code_str,
        success=success,
        output=output_str,
        error=error_msg,
        execution_time_seconds=execution_time
    )

if __name__ == "__main__":
    print("=== Unique Code Execution Engine Demo ===")
    
    # Example 1: Successful execution with printed output
    code_1 = """
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
print("Calculating something complex...")
result = sum(i * i for i in range(1000))
print(f"Result: {result}")
"""

    # Example 2: Code execution containing a runtime error
    code_2 = """
print("Starting buggy process...")
items = [1, 2, 3]
print("Accessing out of bounds item...")
bad_item = items[5]
print("This won't print.")
"""

    print("\nRunning Example 1 (Success Case)...")
    res1 = execute_code = execute_unique_code(code_1)
    print(json.dumps(asdict(res1), indent=2))
    
    print("\nRunning Example 2 (Failure Case)...")
    res2 = execute_unique_code(code_2)
    print(json.dumps(asdict(res2), indent=2))
