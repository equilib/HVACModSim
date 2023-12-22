

from abc import ABC

class VAVTerminalUnit(ABC):
    #use object instance number to automatically tag equipment
    tag_counter = 0

    def __init__(self,
                 min_airflow : float,
                 clg_max_airflow : float,
                 occ_htg_setpoint : float,
                 occ_clg_setpoint : float,
                 unocc_htg_setpoint : float,
                 unocc_clg_setpoint : float) -> None:
       
        super().__init__()
        
        self.set_min_airflow(min_airflow)
        self.set_clg_max_airflow(clg_max_airflow)
        self.set_occ_htg_setpoint(occ_htg_setpoint)
        self.set_occ_clg_setpoint(occ_clg_setpoint)
        self.set_unocc_htg_setpoint(unocc_htg_setpoint)
        self.set_unocc_clg_setpoint(unocc_clg_setpoint)      
        
        VAVTerminalUnit.tag_counter += 1
        self.unit_tag = "VAV-{}".format(VAVTerminalUnit.tag_counter)
    
    def get_tag(self) -> None:
        print(self.unit_tag)

    def set_min_airflow(self, 
                        min_airflow : float) -> None:
        self.__min_airflow = min_airflow
    
    def set_clg_max_airflow(self,
                            clg_max_airflow : float) -> None:
        
        if self.__min_airflow > clg_max_airflow:
            raise Exception("Minimum airflow must be less than cooling max airflow.")
        else:
            self.__clg_max_airflow = clg_max_airflow
        
    def set_occ_htg_setpoint(self,
                             occ_htg_setpoint : float) -> None:
        self.__occ_htg_setpoint = occ_htg_setpoint

    def set_occ_clg_setpoint(self,
                             occ_clg_setpoint : float) -> None:
        self.__occ_clg_setpoint = occ_clg_setpoint        

    def set_unocc_htg_setpoint(self,
                               unocc_htg_setpoint : float) -> None:
        self.__unocc_htg_setpoint = unocc_htg_setpoint

    def set_unocc_clg_setpoint(self,
                               unocc_clg_setpoint : float) -> None:
        self.__unocc_clg_setpoint = unocc_clg_setpoint
    
    def print_summary(self) -> None:
        '''
        '''
        print(f"Unit Tag {self.unit_tag}")
        print(f"Occupied Heating Setpoint (F): {self.__occ_htg_setpoint}")
        print(f"Occupied Cooling Setpoint (F): {self.__occ_clg_setpoint}")
        print(f"Unoccupied Heating Setpoint (F): {self.__unocc_htg_setpoint}")
        print(f"Unoccupied Cooling Setpoint (F): {self.__unocc_clg_setpoint}")
        print(f"Min Airflow (cfm): {self.__min_airflow}")
        print(f"Max Cooling Airflow (cfm): {self.__clg_max_airflow}")

class VAVTerminalUnitReheat(VAVTerminalUnit):

    def __init__(self, 
                 min_airflow: float, 
                 clg_max_airflow: float,
                 htg_max_airflow: float, 
                 occ_htg_setpoint: float, 
                 occ_clg_setpoint: float, 
                 unocc_htg_setpoint: float, 
                 unocc_clg_setpoint: float) -> None:
        super(VAVTerminalUnitReheat,self).__init__(min_airflow, clg_max_airflow, occ_htg_setpoint, occ_clg_setpoint, unocc_htg_setpoint, unocc_clg_setpoint)

        self.set_htg_max_airflow(htg_max_airflow)

    def set_htg_max_airflow(self, htg_max_airflow):
        self.__htg_max_airflow = htg_max_airflow

    def print_summary(self) -> None:
        VAVTerminalUnit.print_summary(self)
        print(f"Max Heating Airflow (cfm) {self.__htg_max_airflow}")


def main():
    vav1 = VAVTerminalUnit(100,150,68,75,60,80)
    vav2 = VAVTerminalUnit(200,250,68,75,60,80)
    vav3 = VAVTerminalUnitReheat(200, 275, 225, 68, 75, 60, 80)

    vav1.print_summary()
    vav2.print_summary()

    vav3.print_summary()


if __name__ == "__main__": 
    main()