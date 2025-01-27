from typing import Dict
import logging

# Set up logger
logger = logging.getLogger(__name__)

class FiniteStateMachine:
    """A generic Finite State Machine implementation."""
    
    def __init__(
        self,
        states: list,
        input_options: list,
        initial_state: str,
        final_states: list,
        transition_function: Dict
    ):
        """
        Initialize the FSM with its components
        
        Args:
            states: List of possible states
            input_options: List of input symbols
            initial_state: Starting state
            final_states: List of final states
            transition_function: Dictionary of state transitions
        """
        logger.info(f"Initializing FSM with states={states}, inputOptions={input_options}")
        logger.debug(f"Initial state: {initial_state}, Final states: {final_states}")

        self.states = states
        self.input_options = input_options
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_function = transition_function
        self.current_state = initial_state
        
        """Validate input_options."""
        # Check if initial state is valid
        if self.initial_state not in self.states:
            logger.error(f"Invalid initial state: {initial_state} not in states list")
            raise ValueError("Initial state must be in states list")
        
        # Check if final states are valid
        for state in self.final_states:
            if state not in self.states:
                logger.error(f"Invalid final state: {state} not in states list")
                raise ValueError("Final states must be in states list")

        logger.info("FSM initialized successfully")
    
    def transition(self, symbol: str) -> str:
        """
        Perform a single transition based on the input symbol.
        
        Args:
            symbol: Input symbol from the input_options
        """
        logger.debug(f"Attempting transition with symbol: {symbol}")
        logger.debug(f"Current state: {self.current_state}")

        if symbol not in self.input_options:
            logger.error(f"Invalid symbol: {symbol} not in inputOptions {self.input_options}")
            raise ValueError(f"Symbol {symbol} not in input_options")
        
        try:
            next_state = self.transition_function[(self.current_state, symbol)]
            logger.info(f"Transition: {self.current_state} --{symbol}--> {next_state}")
            self.current_state = next_state
            return self.current_state
        except KeyError:
            logger.error(f"No transition defined for state {self.current_state} and symbol {symbol}")
            raise ValueError(f"No transition defined for state {self.current_state} and symbol {symbol}")


    def process_input(self, input_sequence: str) -> str:
        """
        Process a sequence of input symbols and return the final state.
        
        Args:
            input_sequence: String of input symbols
        """
        logger.info(f"Processing input sequence: {input_sequence}")
        logger.debug(f"Starting state: {self.current_state}")

        for symbol in input_sequence:
            self.transition(symbol)
        
        logger.info(f"Input sequence processed. Final state: {self.current_state}")
        
        return self.current_state