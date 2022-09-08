from ctypes import (
    CDLL,
    c_uint32,
    c_float,
)
from enum import IntEnum

PATH_PWM_DRIVER = "./driver/pwm.so"
PATH_ADC_DRIVER = "./driver/adc.so"


class PwmType(IntEnum):
    CCS_A = 1,
    CCS_B = 2,


class Pwm:
    def __init__(
            self,
            pwm_type: PwmType = PwmType.CCS_A
    ):
        """
        # TODO : PwmType is for Further Development that we could Configure Multiple pwm by the unique function
        :param pwm_type:
        """
        # Here We Reference Our C driver via ctypes to the python
        self.pwm_type = pwm_type
        self.PwmDriver = CDLL(PATH_PWM_DRIVER)
        self.PwmDriver.ccs_pwm_config.restype = c_uint32
        self.PwmDriver.ccs_pwm_set_duty_cycle.argtypes = [c_uint32, c_float]

        # Here we Config Our Pwm
        self.PwmDriver.ccs_pwm_config(self.pwm_type)

    def Pwm_SetDutyCycle(self, duty_cycle: float):
        self.PwmDriver.ccs_pwm_set_duty_cycle(self.pwm_type, duty_cycle)


class Adc:
    def __init__(self):
        self.AdcDriver = CDLL(PATH_ADC_DRIVER)
        # Function find_device1()
        self.AdcDriver.find_device1.argtype = c_uint32
        self.AdcDriver.find_device1.restype = c_uint32
        # Function read_mean_raw_device1()
        self.AdcDriver.read_mean_raw_device1.argtype = c_uint32
        self.AdcDriver.read_mean_raw_device1.restype = c_uint32
        # Function read_mean_voltage_device1()
        self.AdcDriver.read_mean_voltage_device1.argtype = c_uint32
        self.AdcDriver.read_mean_voltage_device1.restype = c_float

        self._find_device(2)

    def _find_device(self, scale: int):
        self.AdcDriver.find_device1(2)

    def read_raw(self, _time: int) -> int:
        raw = self.AdcDriver.read_mean_raw_device1(_time)
        return raw

    def read_voltage(self) :
        voltage = self.AdcDriver.read_mean_voltage_device1(1)
        voltage = voltage*4
        return voltage


# def main():
#     ccs_a_pwm = Pwm()
#     ccs_a_pwm.Pwm_SetDutyCycle(5)
#     adc = Adc()
#
#     print(adc.read_raw(1))
#     val = adc.read_voltage()
#
#     print(val)
#
#
#     # while True:
#     #     print(adc.read_raw(2))
#     #     time.sleep(1)
#
#
# def run():
#     # asyncio.run(main())
#     main()
#
#
# if __name__ == "__main__":
#     run()


