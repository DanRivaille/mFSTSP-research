drone_info = None

def load_dron_info(filename):
    global drone_info
    names = ['vehicleID', 'vehicleType', 'takeoffSpeed', 'cruiseSpeed', 'landingSpeed', 'yawRageDeg', 'cruiseAlt', 'capacity', 'launchTime', 'recoveryTime', 'serviceTime', 'batteryPower']
    drone_info = pd.read_csv(filename, skiprows=2, names=names)

def getTakeoffSpeed():
    takeoffSpeed = drone_info.iloc[1].takeoffSpeed
    return takeoffSpeed

def getCruiseSpeed():
    cruiseSpeed = drone_info.iloc[1].cruiseSpeed
    return cruiseSpeed

def getLandingSpeed():
    landingSpeed = drone_info.iloc[1].landingSpeed
    return landingSpeed

def getCruiseAlt():
    cruiseAlt = drone_info.iloc[1].cruiseAlt
    return cruiseAlt
    
def getCapacity():
    capacity = drone_info.iloc[1].capacity
    return capacity

def getLaunchTime():
    launchTime = drone_info.iloc[1].launchTime
    return launchTime

def getRecoveryTime():
    recoveryTime = drone_info.iloc[1].recoveryTime
    return recoveryTime

def getBatteryPower():
    batteryPower = drone_info.iloc[1].batteryPower
    return batteryPower

def gerServiceTimeDrone():
    serviceTimeDrone = drone_info.iloc[1].serviceTime
    return serviceTimeDrone

def gerServiceTimeTruck():
    serviceTimeTruck = drone_info.iloc[0].serviceTime
    return serviceTimeTruck

