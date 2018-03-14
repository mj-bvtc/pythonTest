
import progressbar
import time

#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "verbose", default=False, action="store_true", help="Increase verbosity")


progress = progressbar.ProgressBar()

for i in progress(range(200)):
    time.sleep(0.03)

