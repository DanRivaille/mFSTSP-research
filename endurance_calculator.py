from  drone_info_functions import *
import math

def Pi(T, Vvert):
	return 0.8554*T*(Vvert/2.0 + math.sqrt((Vvert/2.0)**2 + T/(0.3051)**2))

def Pp(T):
	return 0.3177*(T**1.5)

def Ppar(Vair):
	return 0.0296*(Vair**3)

def Thrust(m, Vair):  # MATTERNET M2 Weight without payload: 9.5 Kg
	return math.sqrt(((1.5 + m)*9.8 - 0.0279*(Vair*math.cos(10*math.pi/180.0))**2)**2 + (0.0296*Vair**2)**2)


def give_endurance(distance_ij, distance_jk, parcelWtLbs, Etype):
    '''
    Obtiene la duracion restante de un uav
    '''
    # for [v,i,j,k] in P:
    p = getTakeoffSpeed()
    q = getCruiseSpeed()
    r = getLandingSpeed()
    cruiseAlt = getCruiseAlt()

    TTvij = cruiseAlt / getTakeoffSpeed()
    FTvij = distance_ij / getCruiseSpeed()
    LTvij = cruiseAlt / getLandingSpeed()

    TTvjk = cruiseAlt / getTakeoffSpeed()
    FTvjk = distance_jk / getCruiseSpeed()
    LTvjk = cruiseAlt / getLandingSpeed()
    sj = getServiceTimeDrone()
    mj = parcelWtLbs*0.453592   # Weight in Kg
    E = getBatteryPower()

    minimum_time_required = TTvij + FTvij + LTvij + sj + TTvjk + FTvjk + LTvjk

    if Etype == 1:	# Non-linear endurance model
        # a) Takeoff from customer i:
        newT = Thrust(mj, 0)
        Ea = TTvij*(Pi(newT, p) + Pp(newT))

        # b) Fly to customer j:
        newT = Thrust(mj, q)
        Eb = FTvij*(Pi(newT, 0) + Pp(newT) + Ppar(q))

        # c) Land at customer j:
        newT = Thrust(mj, 0)
        Ec = LTvij*(Pi(newT, r) + Pp(newT))

        # d) Takeoff from customer j:
        newT = Thrust(0, 0)
        Ed = TTvjk*(Pi(newT, p) + Pp(newT))

        # e) Fly to customer k:
        newT = Thrust(0, q)
        Ee = FTvjk*(Pi(newT, 0) + Pp(newT) + Ppar(q))

        # f) Land at customer k:
        newT = Thrust(0, 0)
        Ef = LTvjk*(Pi(newT, r) + Pp(newT))

        minimum_energy_required = Ea + Eb + Ec + Ed + Ee + Ef

        energy_left = E - minimum_energy_required

        if energy_left >= 0:
            newT = Thrust(0, 0)
            PHover = Pi(newT, 0) + Pp(newT)

            endurance = minimum_time_required + float(energy_left)/PHover

        else:
            endurance = -1

    elif Etype == 2:	# Linear endurance model
        if q == 31.2928:
            A = 24.2368
            B = 1391.9916

        elif q == 15.6464:
            A = 210.8011
            B = 181.2141

        else:
            print("ERROR: Choose the right vehicle speed")
            exit()

        # Energy required to travel from i to j:
        Eij = (TTvij + FTvij + LTvij)*(A*mj + B)

        # Energy required to travel from j to k:
        Ejk = (TTvjk + FTvjk + LTvjk)*(A*0 + B)

        energy_left = E - (Eij + Ejk)

        if energy_left >= 0:
            endurance = minimum_time_required + float(energy_left)/(A*0 + B)

        else:
            endurance = -1

    elif Etype == 3:	# Fixed endurance (time)
        if int(E) == 291094:
            endurance = 700
        elif int(E) == 562990:
            endurance = 1400
        elif int(E) == 457503:
            endurance = 350
        elif int(E) == 904033:
            endurance = 700

    elif Etype in [4,5]:	# Unlimited endurance in terms of time
        endurance = 24*3600		# 1 Day

    else:
        print('ERROR: Sorry! Wrong endurance type.')
        exit()

    # Se le resta el tiempo minimo requerido para que quede el tiempo restante
    return endurance - minimum_time_required
