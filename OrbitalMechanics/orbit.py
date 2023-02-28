import numpy as np

class Body:
    def __init__(self, rad, m, name = "Planet"):
        self.radius = rad
        self.mass = m
        self.name = name

class Orbit:
    # static class members
    G = 39.478 # AU^3 yr^-2 Ms^-1
    M = 1 # solar mass unit
    # Constructor
    def __init__(self, body:Body, initPos:tuple, initV:tuple, dt:float, B=2.0, a = 1.1e-8):
        self.SetDefaultParamaters(body, initPos, initV, dt, B, a)
        
    # Initiating function (Set all the parameters)
    def SetDefaultParamaters(self, body:Body, initPos:tuple, initV:tuple, dt:float, B, a):
        # Planet
        self.body = body
        self.m = body.mass
        # Position Members ( in AU)
        self.x = initPos[0]
        self.y = initPos[1]
        # Sun-Planet Distance
        self.r = np.sqrt(self.x**2 + self.y**2) 
        # Velocity Members (in AU/yr)
        self.vx = initV[0]
        self.vy = initV[1]
        self.v = np.sqrt(self.vx**2 + self.vy**2)
        self.v_minus1 = 0
        # Beta Constant for Inverse Law
        self.B = B
        # Alpha constant for relativistic Factor
        self.a = a
        # Force Members
        self.fx = (self.G * self.M * self.m) / pow(self.r, self.B + 1.0) \
        * (1+ (self.a/pow(self.r,2))) * self.x
        self.fy = (self.G * self.M * self.m) / pow(self.r, self.B + 1.0) \
        * (1+ (self.a/pow(self.r,2))) * self.y
        self.f = np.sqrt(self.fx**2 + self.fy**2)
        # ENERGY Members
        self.PE = -1 * (self.G*self.M * self.body.mass) / self.r
        self.KE = 0.5 * self.body.mass * pow(self.v, 2)
        self.E = self.KE + self.PE
        # time 
        self.t = 0
        self.dt = dt
        # Period
        self.finishedPeriod = True
    

    def StepOrbit(self):
        # Evaluating PDE's
        self.r = np.sqrt(self.x**2 + self.y**2)
        # Update Forces
        self.fx = (self.G * self.M * self.m) / pow(self.r, self.B + 1.0) \
        * (1+ (self.a/pow(self.r,2))) * self.x
        self.fy = (self.G * self.M * self.m) / pow(self.r, self.B + 1.0) \
        * (1+ (self.a/pow(self.r,2))) * self.y
        self.f = np.sqrt(self.fx**2 + self.fy**2)
        # updating velocity
        self.v_minus1 = self.v # store previous velocity for use in finding period
        self.vx = self.vx - (self.fx / self.body.mass) * self.dt
        self.vy = self.vy - (self.fy / self.body.mass) * self.dt
        self.v = np.sqrt(self.vx**2 + self.vy**2)
        # updating orbit position
        self.x = self.x + (self.vx * self.dt)
        self.y = self.y + (self.vy * self.dt)
        # Update Energy
        self.PE = -1 * (self.G*self.M * self.body.mass) / self.r
        self.KE = 0.5 * self.body.mass * pow(self.v, 2)
        self.E = self.KE + self.PE

    def isAtAphelion(self):
        vAfter = self.v
        vBefore = self.v_minus1
        return ((vAfter - vBefore) > 0)
        
    def isAtPerihelion(self):
        vAfter = self.v
        vBefore = self.v_minus1
        return ((vAfter - vBefore) < 0)

        


    