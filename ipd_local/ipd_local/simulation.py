import random
from tqdm import tqdm

from typing import List, Callable, Any

from .game_specs import *
from .output_locations import *
import types
from loguru import logger

from contextlib import contextmanager
import sys, os

import multiprocessing
import marshal
from collections import defaultdict

@contextmanager
def suppress_stdout():
    """
    Suppresses any writes to stdout.

    Example:
    ```
    print("Suppressing!")
    with suppress_stdout():
        # code to suppress
        strategy() # will not print anything even if it has print statements
    print("Back to normal!")    
    ```
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def pack_functions(functions: Tuple[Callable[..., Any]]) -> Tuple[str]:
    """Packs a tuple of two functions into a tuple of two strings of their bytecode.
    Note:
    - If the function references globals, it will not work!
    - This loses the function name information.    
    """
    return (marshal.dumps(functions[0].__code__), marshal.dumps(functions[1].__code__))


def unpack_functions(bytecodes: Tuple[str]) -> Tuple[Callable[..., Any]]:
    """Unpacks a tuple of two bytecode strings into a tuple of functions.
    Default function names are "p1" and "p2".
    """
    return (
        types.FunctionType(marshal.loads(bytecodes[0]), globals(), "p1"),
        types.FunctionType(marshal.loads(bytecodes[1]), globals(), "p2")
    )


def get_scores(player1_moves: List[bool], player2_moves: List[bool]) -> List[int]:
    """
    TODO
    NOTE This should really return a tuple instead of a list.
    """
    results = [0,0]
    for i in len(player1_moves):            
        if player1moves[i]:
            if player2moves[i]:
                results[0]+=POINTS_BOTH_RAT
                results[1]+=POINTS_BOTH_RAT
            else:
                results[0]+=POINTS_DIFFERENT_LOSER
                results[1]+=POINTS_DIFFERENT_WINNER
        else:
            if player2moves[i]:
                results[0]+=POINTS_DIFFERENT_WINNER
                results[1]+=POINTS_DIFFERENT_LOSER
            else:
                results[0]+=POINTS_BOTH_COOPERATE
                results[1]+=POINTS_BOTH_COOPERATE
                games.append(results)    
    return results

    
def play_match(code_strs: Tuple[str]):
    player1, player2 = unpack_functions(code_strs)        
    # legacy TODO remove
    blindness = [NOISE_LEVEL, NOISE_LEVEL]
    rounds = ROUNDS
    
    games = []
    for _g in range(NOISE_GAMES_TILL_AVG if NOISE else 1): 
        player1moves = []
        player2moves = []
        results=[0,0]


        for i in range(rounds):
            # incorporate noise, if applicable
            # this code can be optimized but since i just took it from someone else i'm just leaving it like this for now
            if blindness[0] > 0:
                if random.random()<blindness[0] and len(player1moves):
                    player1moves[-1] = not(player1moves[-1])
            if blindness[1] > 0:
                if random.random()<blindness[1] and len(player2moves):
                    player2moves[-1] = not(player2moves[-1])

            try:
                with suppress_stdout():
                    player1move = player1(player1moves, player2moves, i)
                    if player1move==None:
                        raise Exception("returned none") # handle None separately because it is cast to False with the bool() function, which is not desired
                    player1move = bool(player1move) # casting allows player to output binary int instead of bool, if desired
            except Exception as e:            
                return None

            try:
                with suppress_stdout():
                    player2move = player2(player2moves, player1moves, i)
                    if player2move==None:
                        raise Exception("returned none")
                    player2move = bool(player2move)
            except Exception as e:
                return None

            player1moves.append(player1move)
            player2moves.append(player2move)

        if len(player1moves) != rounds or len(player2moves) != rounds:
            return None
        
        games.append(get_scores(player1_moves, player2_moves))    

    return [
        sum([g[0] for g in games])/(NOISE_GAMES_TILL_AVG if NOISE else 1),
        sum([g[1] for g in games])/(NOISE_GAMES_TILL_AVG if NOISE else 1),
    ]


def run_simulation_parallel(strats, rounds, blindness):
    matchups = []
    print(len(strats))
    for i,p1 in enumerate(strats):
        for j,p2 in enumerate(strats):
            if j <= i:
                continue
            matchups.append((p1, p2))    
    with multiprocessing.Pool(16) as p:        
        res = list(tqdm(p.imap(
            play_match,
            [pack_functions(x) for x in matchups],            
        ), total=len(matchups)))
    output = defaultdict(dict)
    for i,x in enumerate(matchups):
        match_res = res[i]
        if match_res == None:
            continue
        output[x[0].__name__][x[1].__name__] = match_res
        output[x[1].__name__][x[0].__name__] = list(reversed(match_res))
    return output
