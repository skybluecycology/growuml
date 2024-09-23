from dataclasses import dataclass
import re

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
    for call in method_calls:
        print(f"Executing {call.method} from {call.caller} to {call.callee} with payload {call.payload}")

# Example usage
file_path = 'sequence.plantuml'
method_calls = parse_plantuml(file_path)
execute_methods(method_calls)