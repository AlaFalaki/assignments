from src.remainder import RemainderFiniteStateMachine
import logging

logging.basicConfig(level=logging.INFO) # Or, logging.DEBUG to get all the logs


# Example usage
def main():
    mod_three = RemainderFiniteStateMachine()
    
    # Test cases
    sample_inputs = [
        "110",
        "1010",
    ]
        
    for binary_string in sample_inputs:
        result = mod_three.compute_remainder(binary_string)
        print(f">> Input: {binary_string}, Remainder: {result}")


if __name__ == "__main__":
    main()