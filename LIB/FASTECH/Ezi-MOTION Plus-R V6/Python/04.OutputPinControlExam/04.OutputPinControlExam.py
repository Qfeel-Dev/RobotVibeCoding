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

INPUTPIN = 12
OUTPUTPIN = 10


def Connect(nPortNo: int, dwBaudRate: int) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo, dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess


def SetOutputPin(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print(
        "-----------------------------------------------------------------------------"
    )

    # Check OutputPin Status
    for i in range(OUTPUTPIN):
        status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(
            nPortNo, iSlaveNo, INPUTPIN + i
        )
        if status_result != FMM_OK:
            print("Function(FAS_GetIOAssignMap) was failed.")
            return False

        if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Output Pin[%d] : Logic Mask 0x%08x (%s)"
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )

        else:
            print("Output Pin[%d] : Not Assigned" % i)
    print(
        "-----------------------------------------------------------------------------"
    )

    # Set Output pin Value.
    byPinNo = 3
    byLevel = LEVEL_HIGH_ACTIVE
    dwOutputMask = SERVO_OUT_BITMASK_USEROUT0

    if (
        FAS_SetIOAssignMap(nPortNo, iSlaveNo, INPUTPIN + byPinNo, dwOutputMask, byLevel)
        != FMM_OK
    ):
        print("Function(FAS_SetIOAssignMap) was failed.")
        return False

    # Show Output pins status
    for i in range(OUTPUTPIN):
        status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(
            nPortNo, iSlaveNo, INPUTPIN + i
        )
        if status_result != FMM_OK:
            print("Function(FAS_GetIOAssignMap) was failed.")
            return False

        if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Output Pin[%d] : Logic Mask 0x%08x (%s)"
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )
        else:
            print("Output Pin[%d] : Not Assigned" % i)

    return True


def ControlOutputSignal(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    dwOutputMask = SERVO_OUT_BITMASK_USEROUT0

    print(
        "-----------------------------------------------------------------------------"
    )

    # Control output signal on and off for 60 seconds
    for i in range(30):
        time.sleep(1)
        # USEROUT0: ON
        if FAS_SetIOOutput(nPortNo, iSlaveNo, dwOutputMask, 0) != FMM_OK:
            print("Function(FAS_SetIOOutput) was failed.")
            return False

        time.sleep(1)
        # USEROUT0: OFF
        if FAS_SetIOOutput(nPortNo, iSlaveNo, 0, dwOutputMask) != FMM_OK:
            print("Function(FAS_SetIOOutput) was failed.")
            return False

    print("finish WaitSecond!")
    return True



def main():
    nPortNo = 11
    iSlaveNo = 2
    dwBaudRate = 115200

    # Device Connect
    if not Connect(nPortNo, dwBaudRate):
        input("Press Enter to exit...")
        exit(1)

    # Set Output pin
    if not SetOutputPin(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Control output pin signal
    if not ControlOutputSignal(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
