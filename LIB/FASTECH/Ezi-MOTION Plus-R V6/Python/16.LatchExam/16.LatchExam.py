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

import time


def Connect(nPortNo: int, dwBaudRate: int) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo, dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess


def LatchCount(nPortNo: int, iSlaveNo: int) -> bool:

    cInputNo = 0  # Pin 0

    cntLatchAll = [0] * 16

    print("Monitor a specific pin Input latch signal while 1 min... ")

    # Monitor the specific pin input result value.
    for i in range(600):
        # Latch status
        status_result, uInput, uLatch = FAS_GetInput(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetInput) was failed.")
            return False

        # Latch count
        status_result, nLatchCount = FAS_GetLatchCount(nPortNo, iSlaveNo, cInputNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetLatchCount) was failed.")
            return False

        print(
            "Pin %d is %s and %s (latch count %d)" % (
                cInputNo,
                "ON" if (uInput & (0x01 << cInputNo)) else "OFF",
                "latched" if (uLatch & (0x01 << cInputNo)) else "not latched",
                nLatchCount
            )
        )
        time.sleep(0.1)


    # Clear the specific pin's Latch status
    uLatchMask = 0x01 << cInputNo
    if FAS_ClearLatch(nPortNo, iSlaveNo, uLatchMask) != FMM_OK:
        print("Function(FAS_ClearLatch) was failed.")
        return False
    else:
        print("FAS_ClearLatch Success!")

    # Get Latch status again
    status_result, uInput, uLatch = FAS_GetInput(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Function(FAS_GetInput) was failed.")
        return False
    print(
        "Pin %d is %s" % (
            cInputNo,
            "latched" if (uLatch & (0x01 << cInputNo)) else "not latched"
        )
    )

    # Get latch counts of all inputs (16 inputs)
    status_result, cntLatchAll = FAS_GetLatchCountAll(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Function(FAS_GetLatchCountAll) was failed.")
        return False
    else:
        for i in range(16):
            print("[fas_get_latch_count_all] Pin[%d] : [%d] count" % (i, cntLatchAll[i]))

    # Clear the latch count of the specific pin
    if FAS_ClearLatchCount(nPortNo, iSlaveNo, uLatchMask) != FMM_OK:
        print("Function(FAS_ClearLatchCount) was failed.")
        return False
    else:
        print("FAS_ClearLatchCount Success!")
    return True


def main():
    nPortNo = 11
    iSlaveNo = 2
    dwBaudRate = 115200

    # Device Connect
    if not Connect(nPortNo, dwBaudRate):
        input("Press Enter to exit...")
        exit(1)

    # get input pin latch signal, get a specific pin latch count, get all pin latch count, clear latch
    if not LatchCount(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
