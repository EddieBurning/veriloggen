import sys
import os
from veriloggen import *

def mkLed():
    m = Module('blinkled')
    width = m.Parameter('WIDTH', 8)
    clk = m.Input('CLK')
    rst = m.Input('RST')

    # function to add an LED port
    def add_led(m, postfix, limit=1024):
        led = m.OutputReg('LED'+postfix, width)
        count = m.Reg('count'+postfix, 32)

        m.Always(Posedge(clk))(
            If(rst)(
                count(0)
            ).Else(
                If(count == limit - 1)(
                    count(0)
                ).Else(
                    count(count + 1)
                )
            ))
    
        m.Always(Posedge(clk))(
            If(rst)(
                led(0)
            ).Else(
                If(count == limit - 1)(
                    led(led + 1)
                )
            ))

    # call 'add_led' to add LED ports
    for i in range(4):
        add_led(m, '_' + str(i), limit=i*10 + 10)
    
    return m

if __name__ == '__main__':
    led = mkLed()
    # led.to_verilog(filename='tmp.v')
    verilog = led.to_verilog()
    print(verilog)