from app.environment_settings import env_settings


def greet(name: str) -> str:
    """Return a greeting message for the given name.

    Parameters:
        - name(str): The name of the person to greet

    Returns:
        - str: A greeting message in the format "Hello, {name}!"
    """
    return f"Hello, {name} from {env_settings.cwd}!"


def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.

    Parameters:
        - a(int): First number
        - b(int): Second number

    Returns:
        - int: The sum of a and b
    """
    return a + b


def calculate_factorial(n: int) -> int:
    """Calculate the factorial of a number.

    Uses iterative approach for efficiency.

    NOTE: This function raises ValueError for negative numbers.

    Parameters:
        - n(int): A non-negative integer

    Returns:
        - int: The factorial of n (n!)
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def main() -> None:
    """Main entry point for the application.

    Demonstrates usage of the greet, add_numbers, and calculate_factorial functions.

    Returns:
        - None: This function doesn't return anything
    """
    print("Hello World!")
    print(greet("Developer"))
    print(f"5 + 3 = {add_numbers(5, 3)}")
    print(f"5! = {calculate_factorial(5)}")
