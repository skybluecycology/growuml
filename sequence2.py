from dataclasses import dataclass
import re
import importlib

@dataclass
class MethodCall:
    caller: str
    callee: str
    method: str
    payload: dict

def parse_plantuml(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'(\w+)\s*->\s*(\w+)\s*:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, content)

    method_calls = []
    for match in matches:
        caller, callee, method, payload_str = match
        payload = eval(f"dict({payload_str})") if payload_str else {}
        method_calls.append(MethodCall(caller, callee, method, payload))

    return method_calls

def execute_methods(method_calls):
    # Import your module containing class definitions
    module_name = 'my_classes'
    for call in method_calls:
        try:
            # Dynamically import the class from the module
            module = importlib.import_module(module_name)
            class_ = getattr(module, call.callee)
            
            # Create an instance of the class
            instance = class_()
            
            # Get the method and execute it with the payload
            method = getattr(instance, call.method)
            method(**call.payload)
            
        except AttributeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
file_path = 'sequence.plantuml'
method_calls = parse_plantuml(file_path)
execute_methods(method_calls)