import pytest
from src.FSD import FiniteStateMachine
from src.remainder import RemainderFiniteStateMachine

@pytest.fixture
def basic_fsm():
    """Fixture providing a simple FSM for testing."""
    states = ['S0', 'S1']
    input_options = ['a', 'b']
    initial_state = 'S0'
    final_states = ['S0', 'S1']
    transition_function = {
        ('S0', 'a'): 'S0',
        ('S0', 'b'): 'S1',
        ('S1', 'a'): 'S1',
        ('S1', 'b'): 'S0'
    }
    return FiniteStateMachine(
        states,
        input_options,
        initial_state,
        final_states,
        transition_function
    )

@pytest.fixture
def remainder_fsm():
    """Fixture providing a RemainderFSM instance."""
    return RemainderFiniteStateMachine()

# Tests for FiniteStateMachine
def test_fsm_initialization(basic_fsm):
    """Test proper initialization of FSM."""
    assert basic_fsm.current_state == 'S0'
    assert basic_fsm.states == ['S0', 'S1']
    assert basic_fsm.input_options == ['a', 'b']

def test_invalid_initial_state():
    """Test initialization with invalid initial state."""
    with pytest.raises(ValueError, match="Initial state must be in states list"):
        FiniteStateMachine(
            ['S0', 'S1'],
            ['a', 'b'],
            'INVALID', # <= Invalid initial state
            ['S0', 'S1'],
            {('S0', 'a'): 'S0'}
        )

def test_invalid_final_state():
    """Test initialization with invalid final state."""
    with pytest.raises(ValueError, match="Final states must be in states list"):
        FiniteStateMachine(
            ['S0', 'S1'],
            ['a', 'b'],
            'S0',
            ['INVALID'], # <= Invalid final state
            {('S0', 'a'): 'S0'}
        )

def test_single_transition(basic_fsm):
    """Test single state transition."""
    new_state = basic_fsm.transition('b')
    assert new_state == 'S1'
    assert basic_fsm.current_state == 'S1'

def test_invalid_transition_symbol(basic_fsm):
    """Test transition with invalid input symbol."""
    with pytest.raises(ValueError, match="Symbol INVALID not in input_options"):
        basic_fsm.transition('INVALID')

def test_process_input_sequence(basic_fsm):
    """Test processing a sequence of inputs."""
    final_state = basic_fsm.process_input('aba')
    assert final_state == 'S1'
    assert basic_fsm.current_state == 'S1'


# =====================================
# Tests for RemainderFiniteStateMachine
# =====================================
def test_remainder_fsm_initialization(remainder_fsm):
    """Test proper initialization of RemainderFiniteStateMachine."""
    assert remainder_fsm.fsm.current_state == 'S0'
    assert remainder_fsm.remainder_map['S0'] == 0
    assert remainder_fsm.remainder_map['S1'] == 1
    assert remainder_fsm.remainder_map['S2'] == 2

def test_validate_input_string_valid(remainder_fsm):
    """Test input validation with valid binary string."""
    remainder_fsm.validate_input_string('1010')  # Should not raise

def test_validate_input_string_invalid(remainder_fsm):
    """Test input validation with invalid characters."""
    with pytest.raises(ValueError, match="Invalid character in input"):
        remainder_fsm.validate_input_string('102')

def test_empty_input_string(remainder_fsm):
    """Test handling of empty input string."""
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        remainder_fsm.compute_remainder('')

@pytest.mark.parametrize("binary_string,expected_remainder", [
    ('0', 0),    # 0 mod 3 = 0
    ('1', 1),    # 1 mod 3 = 1
    ('10', 2),   # 2 mod 3 = 2
    ('11', 0),   # 3 mod 3 = 0
    ('100', 1),  # 4 mod 3 = 1
])
def test_compute_remainder_basic(remainder_fsm, binary_string, expected_remainder):
    """Test basic remainder calculations."""
    assert remainder_fsm.compute_remainder(binary_string) == expected_remainder

@pytest.mark.parametrize("binary_string,expected_remainder", [
    ('1010', 1),  # 10 mod 3 = 1
    ('1100', 0),  # 12 mod 3 = 0
    ('1111', 0),  # 15 mod 3 = 0
    ('10000', 1), # 16 mod 3 = 1
    ('10101', 0), # 21 mod 3 = 0
])
def test_compute_remainder_complex(remainder_fsm, binary_string, expected_remainder):
    """Test remainder calculations with longer numbers."""
    assert remainder_fsm.compute_remainder(binary_string) == expected_remainder