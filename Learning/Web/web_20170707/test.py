import time

run = input("Start? > ")
sec = 0
# Only run if the user types in "start"
if run == "start":
    # Loop until we reach 20 minutes running
    while sec != 60:
        print(">", sec)
        # Sleep for a minute
        time.sleep(1)
        # Increment the minute total
        sec += 1
    # Bring up the dialog box here