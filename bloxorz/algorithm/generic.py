import time
import random

from bloxorz.blockstate import Move
from bloxorz.config import generic_algo_config



class Individual:
    CHROMOSOME_LENGTH = generic_algo_config['chromosome_length']
    POPULATION = generic_algo_config['population']
    ELITE_RATE = generic_algo_config['elite_rate']
    MATE_RATE = generic_algo_config['mate_rate']
    MUTATE_RATE = generic_algo_config['mutate_rate']



    def __init__(self, chromosome, game_round):
        self.chromosome = chromosome
        self.game_round = game_round
        self.is_finish = False
        self.max_moves = None
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        visited_coord = set()
        visited_state = set()
        i_state = self.game_round.get_start_state()
        fitness = 0
        moves = []
        is_dead = False
        for move in self.chromosome:
            moves.append(move)
            new_state = self.game_round.calc_new_state(i_state, move)
            if new_state is None:
                # distance = self.game_round.h1_distance(i_state.head, self.game_round.end)
                # fitness += 1 / (1 + distance) * 100
                is_dead = True
                break

            if self.game_round.is_reach_goal(new_state):
                fitness += 1000
                self.is_finish = True
                break
            if new_state.head not in visited_coord and new_state.tail not in visited_coord:
                fitness += 2
            # if new_state not in visited_state:
            #     fitness += 1
            # else:
            #     fitness += -20

            # if self.game_round.h1_distance(new_state.head, self.game_round.end) <  self.game_round.h1_distance(i_state.head, self.game_round.end):
            #     fitness += 20

            visited_coord.add(new_state.head)
            visited_coord.add(new_state.tail)
            visited_state.add(new_state)
            i_state = new_state

        if not is_dead:
            # distance = self.game_round.h1_distance(i_state.head, self.game_round.end)
            # fitness += 1 / (1 + distance) * 100
            fitness += 1 / len(moves) * 100

        self.max_moves = moves
        return fitness

    @classmethod
    def create_rand_individual(cls, game_round):
        chromosome = random.choices(list(Move), k = Individual.CHROMOSOME_LENGTH)
        return cls(chromosome, game_round)

    @staticmethod
    def mutate_chromosome(chromosome):
        chromosome = chromosome.copy()
        mutate_idx = random.randint(0, Individual.CHROMOSOME_LENGTH - 1)
        chromosome[mutate_idx] = random.choice(list(Move))
        return chromosome

    def crossover(self, other):
        min_idx = min(len(self.max_moves), len(other.max_moves))
        split_idx = random.randint(min_idx if min_idx <= Individual.CHROMOSOME_LENGTH - 1 else 1, Individual.CHROMOSOME_LENGTH - 1)
        child = self.chromosome[0:split_idx] + other.chromosome[split_idx:]
        child = Individual.mutate_chromosome(child)
        return Individual(child, self.game_round)

    def __repr__(self):
        return 'Fitness = {}. Move = {}'.format(self.fitness, ' -> '.join(map(lambda x: str(x), self.chromosome)))

class GenericAlgorithm:
    def __init__(self, game_round, timeout):
        self.game_round = game_round
        self.is_found = False
        self.best_moves = None
        self.elapsed_time = 0
        self.solution = None
        self.timeout = timeout

    def get_best_move(self):
        return self.solution.max_moves

    def run(self):

        populations = []
        for _ in range(0, Individual.POPULATION):
            populations.append(Individual.create_rand_individual(self.game_round))

        populations.sort(key=lambda x: x.fitness, reverse=True)
        start = time.time()

        while not self.is_found and (time.time() - start) < self.timeout:

            n_elite = int(Individual.POPULATION * Individual.ELITE_RATE)
            next_generation = populations[0:n_elite]

            n_mate = Individual.POPULATION - n_elite
            for _ in range(0, n_mate):
                mate_range = int(Individual.POPULATION * Individual.MATE_RATE)
                father = random.choice(populations[0:mate_range])
                mother = random.choice(populations[0:mate_range])
                next_generation.append(father.crossover(mother))

            populations = next_generation

            populations.sort(key=lambda x: x.fitness, reverse=True)

            if populations[0].is_finish:
                self.is_found = True
        print(populations[0].max_moves)

        self.solution = populations[0]
        self.elapsed_time = time.time() - start
