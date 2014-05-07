import cmath, random


class Field(object):
    """ Represents the field being walked on."""

    def __init__(self):
        self.walkers = {}

    def add_walker(self, walker, location):
        """ Adds a walker with an initial location. """
        if walker in self.walkers:
            raise ValueError('Duplicate walker!')
        self.walkers[walker] = location

    def move(self, walker):
        """ Updates the location for the walker. """
        if walker not in self.walkers:
            raise ValueError('Walker cannot move since not in field!')
        self.walkers[walker] = self.walkers[walker].move(*walker.take_step())

    def get_location(self, walker):
        """ Get the current location of the walker. """
        if walker not in self.walkers:
            raise ValueError('Walker cannot have location since not in field!')
        return self.walkers[walker]


class Location(object):

    def __init__(self, x, y):
        self.x, self.y = x, y

    def dist_from(self, location):
        """ Gets the distance. """
        return cmath.sqrt((location.x - self.x)**2 +
                    (location.y - self.y)**2).real

    def move(self, dx, dy):
        """ Moves the location by dx and dy. """
        return Location(self.x + dx, self.y + dy)

class Walker(object):
    pass


class GridWalker(Walker):

    def take_step(self):
        """ How the walker walks. """
        choices = [(0.0, 1.0), (1.0, 0.0), (0.0, -1.0), (-1.0, 0.0)]
        return random.choice(choices)

class ColdWalker(Walker):

    def take_step(self):
        """ How the walker walks. """
        choices = [(0.0, 0.99), (1.0, 0.0), (0.0, -1.0), (-1.0, 0.0)]
        return random.choice(choices)


def walk(f, w, num_steps):
    """ Make the walker walk a number of steps.
        Return how far the walker is from origin.
    """
    start = f.get_location(w)
    for _ in range(num_steps):
        f.move(w)
    return start.dist_from(f.get_location(w))


def simulate_walks(num_steps, num_trials, walker_class):
    """ Simulate a walk with num_steps num_trials number of times. """
    distances = []
    for _ in range(num_trials):
        f = Field()
        w = walker_class()
        f.add_walker(w, Location(0,0))
        distances.append(walk(f, w, num_steps))
    return distances


def run_simulation():
    """ Runs the simulation with the specified number of trials. """
    num_trials = 50
    num_steps_list = [100,1000,10000]
    walker_list = [GridWalker, ColdWalker]
    val_list = []
    for walker in walker_list:
        mean_distances = []
        for num_steps in num_steps_list:
            distances = simulate_walks(num_steps, num_trials, walker)
            mean_distances.append(sum(distances)/len(distances))
            print('Random walk of {0} steps'.format(num_steps))
            print('Mean distance is {0}'.format(sum(distances)/len(distances)))
            print('Max distance is {0} and Min distance is {1}'.format(max(distances), min(distances)))
        val_list.append({'num_steps_list': num_steps_list, 'distances': distances, 'mean_distances': mean_distances})
    return val_list

if __name__ == '__main__':
    run_simulation()
