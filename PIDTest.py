import HVACModSim.Controls.PID as PID

import matplotlib.pyplot as plt
import numpy as np

from time import sleep

from math import exp

def T_room(t : float,
           Vdot : float,
           V : float, 
           T0 : float,
           Tsa : float,
           Qdot : float) -> float:
    '''
    Room temperature model
    '''
    

    rho = 0.0763        # lbm/ft^3
    cp = 0.24030        # BTU/lbm-F
    cv = 0.1714         # Btu/lbm-F

    tau = time_constant(cp, cv, V, Vdot)

    T = T0 * exp(-t/tau) + (1 - exp(-t/tau)) * (Qdot/(rho * cp * Vdot) + Tsa)

    return T


def time_constant(cp : float = 0.2403,
                  cv : float = 0.1714,
                  V : float = 100,
                  Vdot : float = 100) -> float:
    
    return (cv * V) / (cp * Vdot)

def clg_af_setpoint(output: float,
                    Vdot_min : float,
                    Vdot_max : float) -> float:
    
    m = (Vdot_max-Vdot_min)/(100-0)
    b = Vdot_max - m * 100

    return min(Vdot_max, max(Vdot_min, m * output + b))

def main():

    # environmental parameters
    cv = 0.1714         # BTU/lbm-F
    V = 10 * 20 * 8     # ft^3
    Vdot_min = 200      # ft^3/min
    Vdot_max = Vdot_min * 3     # ft^3/min
    T0 = 65             # F
    Tsa = 65            # F
    Qdot = 2800         # BTU/hr - net energy transfer into space
    Qdot_min = Qdot / 60# BTU/min
    t = 10              # min

    SP = 70
    deadband = 0
    Kp = 5
    ti = 10
    td = 0

    time = 300          # min
    pv = np.zeros(len(range(0,time)))
    output = np.zeros(len(pv))

    pi = PID.PID(Kp = Kp, ti = ti, td = td, SP = SP, deadband = deadband, action = "direct")

    # initially the output will be 0 for the PID loop
    Vdot = clg_af_setpoint(0, Vdot_min, Vdot_max)

    for t in range(0,len(pv)):

        pv[t] = T_room(t, Vdot, V, T0, Tsa, Qdot_min)
        output[t] = pi.output(pv[t])

        Vdot = clg_af_setpoint(output[t], Vdot_min, Vdot_max)

        print(f"Temperature: {pv[t]}")
        print(f"Airflow: {Vdot}")
        print(f"Error: {pi.error(pv[t])}")
        print(f"output: {output[t]} \n")

        #sleep(np.random.uniform(1,2))
        sleep(0.5)

    plt.plot(pv)
    plt.show()

if __name__ == "__main__":
    main()