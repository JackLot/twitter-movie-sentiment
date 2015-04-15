from __future__ import print_function, division, absolute_import, unicode_literals

import string
import random
import time

# Load in the python wrapper for Vowpal Wabbit
from wabbit_wappa import *

print("Start a Vowpal Wabbit learner in logistic regression mode")
vw = VW(loss_function='logistic')

# Print the command line used for the VW process
print("VW command:", vw.command)
print()

