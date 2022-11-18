import ipd_local
from ipd_local.simulation import *
from ipd_local.default_functions import *
from ipd_local.game_specs import *

def test_suppress_stdout(capsys):
    print("Suppressing!")
    with suppress_stdout():
        print("This shouldn't print!!")
    print("Back to normal!")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Suppressing!\nBack to normal!"

def test_pack_and_unpack_functions():
    def a(): return 2
    def b(x):
        if x > 5: return 10

    packed = pack_functions((a, b))
    assert len(packed) == 2
    assert isinstance(packed[0], bytes)
    assert isinstance(packed[1], bytes)

    a2, b2 = unpack_functions(packed)
    assert a2.__name__ == "p1"
    assert b2.__name__ == "p2"
    assert a2() == 2
    assert b2(3) == None
    assert b2(8) == 10

def test_get_scores():
    assert (
        get_scores([True, False, True], [False, False, True])
        ==
        [
            POINTS_DIFFERENT_WINNER+POINTS_BOTH_RAT+POINTS_BOTH_COOPERATE,
            POINTS_DIFFERENT_LOSER+POINTS_BOTH_RAT+POINTS_BOTH_COOPERATE,
        ]
    )

    assert (
        get_scores([True, False, True], [False, False, True], both_rat=10, both_coop=5)
        ==
        [POINTS_DIFFERENT_WINNER+10+5, POINTS_DIFFERENT_LOSER+10+5]
    )

    assert (
        get_scores([True, False, True], [False, False, True], winner=5, both_coop=5)
        ==
        [5+POINTS_BOTH_RAT+5, POINTS_DIFFERENT_LOSER+POINTS_BOTH_RAT+5]
    )

    assert (
        get_scores([True, False, True], [False, False, True], loser=5, winner=8, both_coop=5)
        ==
        [8+POINTS_BOTH_RAT+5, 5+POINTS_BOTH_RAT+5]
    )

    assert get_scores([], []) == [0,0]

def test_play_match():
    assert (
        play_match(pack_functions((rat, titFortat)), noise=False, rounds=10)
        ==
        [POINTS_DIFFERENT_WINNER + POINTS_BOTH_RAT*9, POINTS_DIFFERENT_LOSER + POINTS_BOTH_RAT*9]
    )

    assert (
        play_match(pack_functions((rat, rat)), noise=True, rounds=10)
        ==
        [POINTS_BOTH_RAT*10, POINTS_BOTH_RAT*10]
    )

    out = play_match(pack_functions((silent, titFortat)), noise=True, rounds=10)
    assert abs((POINTS_BOTH_COOPERATE*9 + POINTS_DIFFERENT_LOSER) - out[0]) < 5
    assert abs((POINTS_BOTH_COOPERATE*9 + POINTS_DIFFERENT_WINNER) - out[1]) < 5

    out = play_match(pack_functions((silent, titFortat)), noise=True, rounds=10, num_games=200)
    assert abs((POINTS_BOTH_COOPERATE*9 + POINTS_DIFFERENT_LOSER) - out[0]) < 1
    assert abs((POINTS_BOTH_COOPERATE*9 + POINTS_DIFFERENT_WINNER) - out[1]) < 1
    
def test_simulation_subsystem():
    # HACK extremely cursed - test behavior dependent on value in game_spec.py (sorry!)
    out = run_simulation([rat, silent, titFortat])
    assert "rat" not in out["rat"]     
    print(out)
    if not ipd_local.game_specs.NOISE:
        assert out == {
            "rat": {
                "silent": [POINTS_DIFFERENT_WINNER*ROUNDS, POINTS_DIFFERENT_LOSER*ROUNDS],
                "titFortat": [
                    POINTS_DIFFERENT_WINNER+POINTS_BOTH_RAT*(ROUNDS-1),
                    POINTS_DIFFERENT_LOSER+POINTS_BOTH_RAT*(ROUNDS-1)
                ]
            },
            "silent": {
                "rat": [POINTS_DIFFERENT_LOSER*ROUNDS, POINTS_DIFFERENT_WINNER*ROUNDS],
                "titFortat": [POINTS_BOTH_COOPERATE*ROUNDS, POINTS_BOTH_COOPERATE*ROUNDS],
            },
            "titFortat": {
                "rat": [
                    POINTS_DIFFERENT_LOSER+POINTS_BOTH_RAT*(ROUNDS-1),
                    POINTS_DIFFERENT_WINNER+POINTS_BOTH_RAT*(ROUNDS-1)
                ],
                "silent": [POINTS_BOTH_COOPERATE*ROUNDS, POINTS_BOTH_COOPERATE*ROUNDS],
            },
        }
    else:
        assert out["rat"]["silent"] == [POINTS_DIFFERENT_WINNER*ROUNDS, POINTS_DIFFERENT_LOSER*ROUNDS]
        assert out["silent"]["rat"] == [POINTS_DIFFERENT_LOSER*ROUNDS, POINTS_DIFFERENT_WINNER*ROUNDS]

        res = out["silent"]["titFortat"]
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10)) - res[0]) < 5
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10)) - res[1]) < 5
        res = out["titFortat"]["silent"]
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10)) - res[0]) < 5
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10)) - res[1]) < 5

        res = out["rat"]["titFortat"]
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10 + 1)) - res[0]) < 10
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10 + 1)) - res[1]) < 10
        res = out["titFortat"]["rat"]
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10 + 1)) - res[0]) < 10
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10 + 1)) - res[1]) < 10

