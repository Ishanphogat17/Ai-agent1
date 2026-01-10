from functions.get_file_content import get_file_content
from config import MAX_CHARS

print('Testing get_file_content("calculator", "lorem.txt"):')
content = get_file_content("calculator", "lorem.txt")
print(f"Content length: {len(content)}")
print(f"Truncated message present: {'truncated at' in content}")
print(content[-100:]) # Print last 100 chars to verify logic
print()

print('Testing get_file_content("calculator", "main.py"):')
print(get_file_content("calculator", "main.py")[:200]) # Print first 200 chars
print()

print('Testing get_file_content("calculator", "pkg/calculator.py"):')
print(get_file_content("calculator", "pkg/calculator.py")[:200]) # Print first 200 chars
print()

print('Testing get_file_content("calculator", "/bin/cat"):')
print(get_file_content("calculator", "/bin/cat"))
print()

print('Testing get_file_content("calculator", "pkg/does_not_exist.py"):')
print(get_file_content("calculator", "pkg/does_not_exist.py"))
