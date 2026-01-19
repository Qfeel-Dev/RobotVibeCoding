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


def Connect(nPortNo: int, dwBaudRate: int) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo, dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess


def SetInputPin(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print(
        "-----------------------------------------------------------------------------"
    )

    # Set Input pin Value.
    byPinNo = 3
    byLevel = LEVEL_LOW_ACTIVE
    dwInputMask = SERVO_IN_BITMASK_USERIN0

    if FAS_SetIOAssignMap(nPortNo, iSlaveNo, byPinNo, dwInputMask, byLevel) != FMM_OK:
        print("Function(FAS_SetIOAssignMap) was failed.")
        return False
    else:
        print(
            "SERVO_IN_BITMASK_USERIN0 (Pin%d) : [%s]"
            % (byPinNo, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
        )

    print(
        "-----------------------------------------------------------------------------"
    )

    # Show Input pins status
    for i in range(INPUTPIN):
        status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(nPortNo, iSlaveNo, i)
        if status_result != FMM_OK:
            print("Function(FAS_GetIOAssignMap) was failed.")
            return False
        if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Input PIN[%d] : Logic Mask 0x%08x (%s)"
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )

        else:
            print("Input Pin[%d] : Not Assigned" % i)

    return True


def CheckInputSignal(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    dwInputMask = SERVO_IN_BITMASK_USERIN0

    print(
        "-----------------------------------------------------------------------------"
    )
    # When the value SERVO_IN_BITMASK_USERIN0 is entered with the set PinNo, an input confirmation message is displyed.
    # Monitoring input signal for 60 seconds
    for i in range(600):
        status_result, dwInput = FAS_GetIOInput(nPortNo, iSlaveNo)
        if status_result == FMM_OK:
            if dwInput & dwInputMask:
                print("INPUT PIN DETECTED.")
        else:
            print("Function(FAS_GetIOInput) was failed.")
            return False
        time.sleep(0.1)
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

    # Set Input pins
    if not SetInputPin(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Check Input Pin Signal
    if not CheckInputSignal(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
