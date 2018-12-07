# Auxiliary functions
from math import factorial
import pygame
from const import *
from random import randint


# binom and binom_list are to produce a curve used to smooth out movement
# (so things don't scroll at constant speed)
def binom(n, p, k):
    """
    calculates probability subjected to binomial distrobution
    returns the probability of k positive results out of n tests, where the probability of having a positive result
    in a test is p.
    :param n: int
    :param p: float
    :param k: int
    :return: float
    """

    def nCr(n, r):
        f = factorial
        return f(n) / (f(n - r) * f(r))

    return nCr(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binom_list(length):
    """
    return a list of length n where the elements follows the binomial distribution curve and sums to 1
    :param length: int
    :return: list
    """
    list = []
    for i in range(length):
        list.append(binom(length, 0.5, i))
    return list


# Highscore
def read_highscore(filename):
    score_list = []
    f = open(filename, "r")
    for line in f:
        score_list.append(int(line))
    f.close()
    # print(score_list,"a")
    return score_list


def insert_into_highscore(score, list):
    list.append(score)
    list.sort(reverse=True)
    return list


def update_highscore(filename, score_list):
    f = open(filename, "w")
    i = 0
    for item in score_list:
        if i < 20:
            f.write(str(item) + "\n")
            i += 1
    f.close()

# random
def rand_platform_x():
    """
    returns a
    :return: int
    """
    return randint(PLATFORM_WIDTH / 2, CAMERA_WIDTH - (PLATFORM_WIDTH / 2) + 1)

state = 0
def toggle(n):
    global state
    state = (state+1)%n
    return state