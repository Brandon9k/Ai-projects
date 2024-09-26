#Program designed to solve Travelling Salesman problem with Ant Colony Optimization

import random, datetime, math
# import matplotlib.pyplot as plt

# Current time and title of the project for the index
def logFormat():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    printFormat = '[' + str(now) + ']' + '[TSP_ACO]| > '
    return printFormat

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distanceBetween(self, city):
        distanceX = abs(self.x - city.x)
        distanceY = abs(self.y - city.y)

        return math.sqrt(distanceX**2 + distanceY**2)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ant:
    def __init__(self, colony, alpha, beta):
        self.colony = colony
        self.alpha = alpha
        self.beta = beta
        self.visited = []
        self.distance = 0
    
    def nextCity(self):
        currentCity = self.visited[-1]
        unvisitedCities = [city for city in self.colony.cities if city not in self.visited]
        probabilities = []
        total = 0

        # Calculate attractiveness of each unvisited city based on pheromone and distance
        for city in unvisitedCities:
            pheromone = self.colony.pheromoneMatrix[currentCity][city]
            distance = currentCity.distanceBetween(city)
            attractiveness = (pheromone**self.alpha) * ((1/distance)**self.beta)
            probabilities.append(attractiveness)
            total += attractiveness
        
        probabilities = [p / total for p in probabilities]
        nextCity = random.choices(unvisitedCities, probabilities)[0]
        
        return nextCity
    
    def tour(self):
        while len(self.visited) < len(self.colony.cities):
            nextCity = self.nextCity()
            self.visited.append(nextCity)
            self.distance += self.visited[-2].distanceBetween(nextCity)
        
        self.distance += self.visited[-1].distanceBetween(self.visited[0])
    
    def depositPheromone(self):
        pheromoneDeposit = 1 / self.distance
        
        # Deposit pheromone on each edge of the visited route
        for i in range(len(self.visited) - 1):
            cityA = self.visited[i]
            cityB = self.visited[i + 1]
            self.colony.pheromoneMatrix[cityA][cityB] += pheromoneDeposit
            self.colony.pheromoneMatrix[cityB][cityA] += pheromoneDeposit

class TravelingSalesmanProblemACO:
    def __init__(self, numberCities=25, populationSize=100, generations=500, alpha=1, beta=5, evaporationRate=0.5):
        self.numberCities = numberCities
        self.populationSize = populationSize
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.evaporationRate = evaporationRate

        self.cities = []
        self.pheromoneMatrix = {}
        self.fastestRoutes = []
        self.bestDistance = float('inf')
    
    def initializeCities(self):
        # Randomly generate cities with coordinates within a range
        print(logFormat() + "[1/5] Initializing cities")
        for _ in range(self.numberCities):
            city = City(x=int(random.random() * 200), y=int(random.random() * 200))
            self.cities.append(city)
    
    def initializePheromoneMatrix(self):
        # Initialize the pheromone matrix with default pheromone levels
        print(logFormat() + "[2/5] Initializing pheromone matrix")
        for cityA in self.cities:
            self.pheromoneMatrix[cityA] = {}
            for cityB in self.cities:
                self.pheromoneMatrix[cityA][cityB] = 1
    
    def evaporatePheromones(self):
        # Evaporate pheromones on all edges based on the evaporation rate
        for cityA in self.cities:
            for cityB in self.cities:
                self.pheromoneMatrix[cityA][cityB] *= (1 - self.evaporationRate)
    
    def runAnts(self):
        ants = [Ant(self, self.alpha, self.beta) for _ in range(self.populationSize)]

        for ant in ants:
            # Start with a random city
            ant.visited = [random.choice(self.cities)]
            ant.tour()
            ant.depositPheromone()

            if ant.distance < self.bestDistance:
                # Update the best route if a shorter route is found
                self.bestDistance = ant.distance
                self.fastestRoutes = ant.visited
    
    def filterFastestRoutes(self):
        # Filtering to increase the chances of a perfect route
        if self.bestDistance < 700:
            print(logFormat() + f"Best route: {self.fastestRoutes}")
    
    def run(self):
        self.initializeCities()
        self.initializePheromoneMatrix()

        print(logFormat() + "[3/5] Filtering routes")
        for _ in range(self.generations):
            self.runAnts()
            self.evaporatePheromones()
            self.filterFastestRoutes()

        self.plotFastestRoutes()
    
    def plotFastestRoutes(self):
        print(logFormat() + "[4/5] Finalizing plotting")
        # Plotting the cities and fastest routes
        x = [city.x for city in self.fastestRoutes]
        y = [city.y for city in self.fastestRoutes]
        
        plt.figure(num='Traveling Salesman Problem (ACO)', figsize=(8, 6))
        plt.scatter(x, y, c='b', marker='o')
        plt.plot(x + [x[0]], y + [y[0]], c='r', linestyle='-', linewidth=1)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Traveling Salesman Problem (ACO)')
        plt.grid(True)
        print(logFormat() + "[5/5] Check plot")
        plt.show()
        
if __name__ == "__main__":
    tsp = TravelingSalesmanProblemACO()
    tsp.run()
