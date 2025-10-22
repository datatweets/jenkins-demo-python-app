"""
Main application module for Jenkins Demo
"""

def greet(name):
    """Return a greeting message"""
    if not name:
        raise ValueError("Name cannot be empty")
    return f"Hello, {name}!"

def add(a, b):
    """Add two numbers"""
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def main():
    """Main entry point"""
    print("🚀 Jenkins Demo Python App")
    print(greet("Jenkins"))
    print(f"2 + 3 = {add(2, 3)}")
    print(f"4 * 5 = {multiply(4, 5)}")

if __name__ == "__main__":
    main()
