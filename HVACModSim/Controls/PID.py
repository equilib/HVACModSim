import time
import numpy as np
import matplotlib.pyplot as plt

class PID:

    __controller_action = {"direct" : 1, "reverse" : -1}

    def __init__(self,
                 Kp : float = 1.0,
                 ti : float = 0.0,
                 td : float = 0.0,
                 bias : float = 0.0,
                 deadband : float = 0.0,
                 SP : float = 0.0,
                 output_min : float = 0.0,
                 output_max : float = 100.0,
                 action : str = "direct") -> None:
        '''
        
        '''
        
        self.__Kp, self.__ti, self.__td = Kp, ti, td
        self.__Ki = self.__Kp / self.__ti
        self.__Kd = self.__Kp * self.__td
        self.__bias, self.__deadband = bias, deadband
        self.__SP = SP
        self.__output_min, self.__output_max = output_min, output_max
        self.__action = self.__controller_action[action]          # control loop action: direct action = 1 / reverse action = -1
        
        self.__prev_error = 0.0
        self.__prev_time = time.time()
        self.__dt = 0.1         # sample time (s)
        self.__I = 0.0

    def P(self,
          PV : float = 0.0) -> float:
        
        return (self.__Kp * self.error(PV))

    def I(self,
          PV : float = 0.0) -> float:
        '''
        Integrate by trapazoid rule: A = 1/2 (a + b) * h
        h = t_i - t_i-1
        a = e(t_i-1)
        b = e(t_i)
        @todo - Review coding of integration scheme and accumulation
        '''
        t_1 = self.__prev_time
        t_2 = time.time()
        self.__prev_time = t_2
        delta_t = t_2 - t_1

        e_1 = self.__prev_error
        e_2 = self.error(PV)

        self.__I += self.__Ki * (0.5 * (e_2 + e_1) * delta_t)
        return self.__I

    def D(self,
          PV : float = 0.0) -> float:
        '''
        Approximate time derivative of error by small time step
        de/dt ~= (e(t_i) - e(t_i-1)) / dt
        '''

        e_1 = self.__prev_error
        e_2 = self.error(PV)
        dt = self.__dt

        de_dt = (e_2 - e_1) / dt

        return self.__Kd * de_dt
    
    def error(self,
              PV : float = 0.0) -> float:
        '''
        @todo - review coding of error calc to ensure correct value for correct action
        '''

        # direct acting control with deadband
        if self.__action == 1: # direct acting
            return (-1 * ((self.__SP + self.__deadband / 2) - PV))
        else: # reverse acting
            return ((self.__SP - self.__deadband / 2) - PV)

        #return ((self.__SP - self.__deadband / 2) - PV)
    
    def output(self,
               PV : float) -> float:
        
        u_t = self.P(PV) + self.I(PV) + self.D(PV) + self.__bias

        return self.__minmax(u_t)

    def reset(self) -> float:

        self.__Kp, self.__Ki, self.__Kd = 0.0
    
    def tune(self,
             Kp : float,
             Ki : float,
             Kd : float,
             bias : float) -> None:
        
        self.__Kp = Kp if Kp != None else self.__Kp
        self.__Ki = Ki if Ki != None else self.__Ki
        self.__Kd = Kd if Kd != None else self.__Kd
        self.__bias = bias if bias != None else self.__bias

    def setpoint_adjust(self,
                        SP : float) -> None:
        
        if SP != None:
            self.__SP = SP

    def setpoint(self) -> float:

        return self.__SP
    
    def __minmax(self,
               val : float) -> float:

        return max(self.__output_min, min(self.__output_max, val))


def main():

    PV = 68
    SP = 72
    deadband = 2
    Kp = 1
    ti = 1
    td = 0

    pv = np.zeros(len(range(0,20)))
    output = np.zeros(len(pv))

    pid = PID(Kp = Kp, ti = ti, td = td, SP = SP, deadband = deadband, action = "reverse")

    for i in range(0,20):
        PV = np.random.uniform(66,74)
        pv[i] = PV
        output[i] = pid.output(PV)
        print(f"PV: {PV}")
        print(f"Error: {pid.error(PV):.3f}")
        print(f"Proportional: {pid.P(PV):.3f}")
        print(f"Integral: {pid.I(PV):.3f}")
        print(f"Derivative: {pid.D(PV):.3f}")
        print(f"Output: {pid.output(PV):.3f}")
        print("\n")
        time.sleep(np.random.uniform(1,3))

    print(np.mean(pv))

    fig = plt.figure(1, figsize=(10,6))  
    ax = fig.add_subplot(111)  
    ax.plot(pv, color='red')
    ax.set_ylabel("Deg F")
    ax.legend(["process variable"], loc='lower right')

    ax2 = ax.twinx()
    ax2.set_ylabel("%")
    ax2.plot(output, color='green')
    ax2.set_ylim(bottom = 0.0, top = 100.0)

    ax2.legend(["output"])
    plt.show()



if __name__ == "__main__":
    main()