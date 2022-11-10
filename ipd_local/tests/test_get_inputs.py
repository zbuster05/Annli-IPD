from ipd_local.get_inputs import *

def test_get_inputs():
    """Subsystem test for the input handling subsystem of the library."""
    strats, rounds, blindness = get_game_inputs()
    
    assert [callable(strat) for strat in strats ] == [True]*TODOgit
    assert [strat.__name__ for strat in strats] == TODO    
    
    assert rounds == ROUNDS
    assert blindness == [NOISE_LEVEL, NOISE_LEVEL]

