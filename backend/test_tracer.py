from utils.tracer import trace_execution

code = """
numbers = [1, 2, 3]
for n in numbers:
    print(n)
"""

trace, output = trace_execution(code)

print("TRACE:")
for step in trace:
    print(step)

print("\nOUTPUT:")
print(output)
