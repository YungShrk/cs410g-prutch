# Filename: calculator.py
def add(a, b):
    """
    Add two numbers.
    Args:
        a (int): First number.
        b (int): Second number.
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

def subtract(a, b):
    """
    Subtract two numbers.
    Args:
        a (int): First number.
        b (int): Second number.
    Returns:
        int: The result of subtracting b from a.
    """
    return a - b

if __name__ == "__main__":
    x = 10
    y = 5
    print(f"Add: {add(x, y)}")
    print(f"Subtract: {subtract(x, y)}")

