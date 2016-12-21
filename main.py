#!/usr/bin/env python
from random import randint
from time import sleep
from uuid import uuid4 as RandomUUID

airport_list = []
plane_list = []


class Plane(object):
    name = None
    capacity = -1
    current_airport = None
    passengers = []
    destination = None

    def __init__(self, capacity=None, current_airport=None):
        self.name = str(RandomUUID())
        self.capacity = capacity
        self.current_airport = current_airport

        if not self.capacity:
            self.capacity = randint(1, 100)

        print self.current_airport.name


    def __str__(self):
        return "%s (%s)" % (self.name[-6:], self.current_airport.name)



class Passenger(object):
    destination = None


class Airport(object):
    name = None
    passengers = []
    aircraft = []
    priority = 1
    passenger_spawn_rate = 0
    location = (0, 0)

    def __init__(self):
        self.name = str(RandomUUID()).upper()
        self.location = (randint(0, 1000), randint(0, 1000))

    def __str__(self):
        name = self.name[-8:]
        pax = len(self.passengers)
        aircraft = ''.join(["%s (%d)\n" % (craft.name[-4:], craft.capacity) for craft in self.aircraft])

        return "%s - %d\n------\n%s" % (name, pax, aircraft)


class Simulation(object):
    planes = []
    airports = []
    ticks = 0

    def __init__(self):
        for i in range(10):
            air = Airport()
            air.priority = randint(1, 10)
            air.passenger_spawn_rate = randint(1, 10)
            self.airports.append(air)

        for i in range(3):
            plane = Plane(1, self.airports[randint(0, len(self.airports) - 1)])
            print plane
            self.planes.append(plane)


    def do_tick(self):
        self.ticks += 1

        for plane in self.planes:
            # offload passengers
            # TODO: record this in stats
            for pax in plane.passengers[:]:
                if pax.destination == plane.current_airport:
                    plane.passengers.remove(pax)

            # move the planes instantaneoeusously - TODO speed?
            if not plane.current_airport == plane.destination:
                plane.current_airport = plane.destination
                # TODO update airport.planes - why the heck does this not work? where did current_airport disappear to??
                print plane.name
                print plane.current_airport
                plane.current_airport.planes.append(plane)


        for airport in self.airports:
            # spawn new passengers with a new destination
            if self.ticks % airport.passenger_spawn_rate:
                pss = Passenger()
                pss.destination = airport
                while pss.destination == airport:
                    # TODO - use priority of airport in determinig destination
                    pss.destination = self.airports[randint(0, len(self.airports) - 1)]

        self.schedule_flights()


    def schedule_flights(self):
       pass


    def display(self):
        for airport in self.airports:
            print airport

        print '-' * 15

        for plane in self.planes:
            print plane



s = Simulation()
for i in range(2):
    s.do_tick()
    s.display()
    sleep(1)


