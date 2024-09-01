
import rp2
import machine
import time

# Define the PIO program for generating square waves with a 1:1 duty ratio
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def square_wave():
    pull()                    # Pull value from TX FIFO
    
    label("loop")             # Start of the loop    
    mov(x, osr)               # Move the pulled value to X register (used for delay)
    nop()   .side(1) [0]      # Set GPIO high
    label("high_delay")
    jmp(x_dec, "high_delay")  # Decrement X and loop until X reaches 0 (high state duration)
    jmp("low_state")          # Once X is 0, move to low state

    label("low_state")
    mov(x, osr)               # Reset X with the delay value for the low state
    nop()   .side(0) [0]      # Set GPIO low
    label("low_delay")
    jmp(x_dec, "low_delay")   # Decrement X and loop until X reaches 0 (low state duration)
    jmp("loop")               # Once X is 0, restart the loop


# Setup PIO and state machine
sm = rp2.StateMachine(0, square_wave, freq=125000000, sideset_base=machine.Pin(15))  # Set GPIO pin 15 as output

# Start the state machine with a delay count for the frequency
delay = 31  # Adjust delay for the desired frequency
sm.put(delay)
sm.active(1)

print(f"State machine active: {sm.active()}")
print(f"Delay value used: {delay}")
# Run the square wave for a period of time
#time.sleep(10)

# Stop the state machine
#sm.active(0)

