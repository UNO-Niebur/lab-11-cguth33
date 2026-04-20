# StopLightSim.py
# Name: Carter Guthrie
# Date: 4/19/2026
# Assignment: Lab 11

import simpy

# Global variable to track light state
# True means cars can go, False means they must wait
greenLight = True

def stopLight(env):
    """Simulates a traffic light that cycles between green, yellow, and red."""
    global greenLight
    
    while True:
        # Green Phase
        print(f"Green at time {env.now}")
        greenLight = True
        yield env.timeout(30)
        
        # Yellow Phase
        print(f"Yellow at time {env.now}")
        # Typically cars should stop for yellow in sims, 
        # so we set this to False here.
        greenLight = False 
        yield env.timeout(2)
        
        # Red Phase
        print(f"Red at time {env.now}")
        greenLight = False
        yield env.timeout(20)

def car(env, car_id):
    """Simulates a car arriving and waiting for the light."""
    print(f"Car {car_id} arrived at {env.now}")

    # Check the global light status
    # If the light is not green, the car "waits" by yielding a small timeout
    while not greenLight:
        yield env.timeout(1)

    print(f"Car {car_id} departed at {env.now}")

def carArrival(env):
    """Creates cars at regular intervals."""
    car_id = 0
    while True:
        car_id += 1
        # Start the individual car process
        env.process(car(env, car_id))
        
        # Wait 5 time units before the next car arrives
        yield env.timeout(5)

def main():
    # Create the SimPy environment
    env = simpy.Environment()

    # Start the background processes
    env.process(stopLight(env))
    env.process(carArrival(env))

    # Run simulation for the required 100 time units
    print("Starting Simulation...")
    env.run(until=100)
    print("Simulation complete")

if __name__ == "__main__":
    main()