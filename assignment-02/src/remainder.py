from src.FSD import FiniteStateMachine
import logging

# Set up logger
logger = logging.getLogger(__name__)

class RemainderFiniteStateMachine:
    """Implementation of the mod-three problem using the generic FSM."""
    
    def __init__(self):
        """Initialize the mod-three FSM with its specific configuration."""
        logger.info("Initializing RemainderFiniteStateMachine")

        states = ['S0', 'S1', 'S2']
        input_options = ['0', '1']
        initial_state = 'S0'
        final_states = ['S0', 'S1', 'S2']
        
        transition_function = {
            ('S0', '0'): 'S0',
            ('S0', '1'): 'S1',
            ('S1', '0'): 'S2',
            ('S1', '1'): 'S0',
            ('S2', '0'): 'S1',
            ('S2', '1'): 'S2'
        }

        logger.debug("Creating FSM instance with transition function:")
        for (state, symbol), next_state in transition_function.items():
            logger.debug(f"  {state} --{symbol}--> {next_state}")

        
        # Create the FSM instance
        self.fsm = FiniteStateMachine(states, input_options, initial_state, final_states, transition_function)
        
        # Map final states to remainder values
        self.remainder_map = {
            'S0': 0,
            'S1': 1,
            'S2': 2
        }
        logger.info("RemainderFiniteStateMachine initialized successfully")
    
    def validate_input_string(self, binary_string: str) -> bool:
        """
        Validate the input string to ensure it only contains 1's and 0's.
        
        Args:
            binary_string: String of 1's and 0's representing a binary number
        """
        logger.debug(f"Validating input string: {binary_string}")

        # Check if string only contains 0s and 1s
        for char in binary_string:
            if char not in ['0', '1']:
                logger.error(f"Invalid character '{char}' in input string")
                raise ValueError(f"Invalid character in input. Only '0' and '1' are allowed")

        logger.debug("Input string validation successful")

    def compute_remainder(self, binary_string: str) -> int:
        """
        Compute the remainder when the binary number is divided by 3.
        
        Args:
            binary_string: String of 1's and 0's representing a binary number
        """
        logger.info(f"Computing remainder for binary string: {binary_string}")

        if not binary_string:
            logger.error("Empty input string provided")
            raise ValueError("Input string cannot be empty")

        self.fsm.current_state = self.fsm.initial_state
        logger.debug("FSM reset to initial state")

        self.validate_input_string(binary_string)

        final_state = self.fsm.process_input(binary_string)
        remainder = self.remainder_map[final_state]

        logger.info(f"Computation complete. Binary: {binary_string} ≡ {remainder} (mod 3)")

        return remainder