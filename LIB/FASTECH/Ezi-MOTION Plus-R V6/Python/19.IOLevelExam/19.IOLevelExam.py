#####################################################
# Version: 1.0.0                                    #
# Last modified date: 25.10.31                      #
# Changes log: First released version               #
#####################################################


#*************************************************************************************************************************************
#** Notification before use																											**
#*************************************************************************************************************************************
#** Depending on the type of product you are using, the definitions of Parameter, IO Logic, AxisStatus, etc. may be different.		**
#** This example is based on Ezi-SERVO, so please apply the appropriate value depending on the product you are using.				**
#*************************************************************************************************************************************
#** ex)	FM_EZISERVO_PARAM			// Parameter enum when using Ezi-SERVO						 									**
#**		FM_EZIMOTIONLINK_PARAM		// Parameter enum when using Ezi-MOTIONLINK														**
#*************************************************************************************************************************************

import sys
import os
import platform
try:
    include_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
except NameError:
    include_path = os.path.abspath(
        os.path.join(os.getcwd(), "..")
    )

arch = platform.architecture()[0]
if arch == '64bit':
    library_path = os.path.join(include_path, "Include_Python_x64")
else:
    library_path = os.path.join(include_path, "Include_Python")

sys.path.append(library_path)

from FAS_EziMOTIONPlusR import *
from MOTION_DEFINE import *
from ReturnCodes_Define import *
from MOTION_EziSERVO_DEFINE import *


def Connect(nPortNo: int, dwBaudRate: int) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo, dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess


def GetIOLevel(nPortNo: int, iSlaveNo: int) -> bool:

    print("----------------------------------")
    # [Before] Check IO Level Status
    status_result, uIOLevel = FAS_GetIOLevel(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Function(FAS_GetIOLevel) was failed.")
        return False
    print("Load IO Level Status : 0x%08x" % uIOLevel)
    for i in range(16):
        bLevel = (uIOLevel & (0x01 << i)) != 0
        print("I/O pin %d : %s" % (i, "High Active" if bLevel else "Low Active"))
    return True


def SetIOLevel(nPortNo: int, iSlaveNo: int) -> bool:

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~ Fastech's product which has Input (or Output) only (Ezi-IO-I16, Ezi-IO-O16, Ezi-IO-I32, Ezi-IO-O32...), BitMask of Input (or Output) starts from 0x01,	~~
    # ~~ However, for Input+Output mixed products (Ezi-IO-I8O8, Ezi-IO-I16O16, etc.), the BitMask of Output is allocated after the BitMasks of Input.			~~
    # ~~ Ezi-IO-I8O8, for example, the BitMask of Input 0 is 0x0001, and the BitMask of Output 0 is 0x0100.														~~
    # ~~ For detailed allocation methods, please refer to Section 2.3 of the "doc.md" file of this example.														~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    uIOLevel = 0x0000FF00

    print("----------------------------------")

    # Set IO Level Status
    if FAS_SetIOLevel(nPortNo, iSlaveNo, uIOLevel) != FMM_OK:
        print("Function(FAS_SetIOLevel) was failed.")

    else:
        print("Set IO Level Status : 0x%08x" % uIOLevel)
    return True


def main():
    nPortNo = 11
    iSlaveNo = 2
    dwBaudRate = 115200

    # Device Connect
    if not Connect(nPortNo, dwBaudRate):
        input("Press Enter to exit...")
        exit(1)

    # Get IO Level
    if not GetIOLevel(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Set IO Level
    if not SetIOLevel(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
