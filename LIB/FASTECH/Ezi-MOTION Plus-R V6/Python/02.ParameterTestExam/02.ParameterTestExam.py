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


def SetParameter(nPortNo: int, iSlaveNo: int) -> bool:
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    nChangeValue = 100

    print(
        "-----------------------------------------------------------------------------"
    )
    # Check The Axis Start Speed Parameter Status
    status_result, lParamVal = FAS_GetParameter(nPortNo, iSlaveNo, SERVO_AXISSTARTSPEED)
    if status_result != FMM_OK:
        print("Function(FAS_GetParameter) was failed.")
        return False
    else:
        print("Load Parameter[Before] : Start Speed = %d[pps]" % lParamVal)


    print(
        "-----------------------------------------------------------------------------"
    )
    # Change the (Axxis Start Speed Parameter) vlaue to (nChangeValue) value.
    status_result = FAS_SetParameter(
        nPortNo, iSlaveNo, SERVO_AXISSTARTSPEED, nChangeValue
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetParameter) was failed.")
        return False
    else:
        print("Set Parameter: Start Speed = %d[pps]" % nChangeValue)

    print(
        "-----------------------------------------------------------------------------"
    )
    # Check the changed Axis Start Speed Parameter again.
    status_result, lParamVal = FAS_GetParameter(nPortNo, iSlaveNo, SERVO_AXISSTARTSPEED)
    if status_result != FMM_OK:
        print("Function(FAS_GetParameter) was failed.")
        return False
    else:
        print("Load Parameter[After] : Start Speed = %d[pps]" % lParamVal)

    return True


def main():
    nPortNo = 11
    iSlaveNo = 2
    dwBaudRate = 115200

    # Device Connect
    if not Connect(nPortNo, dwBaudRate):
        input("Press Enter to exit...")
        exit(1)

    # Load and Set Parameter
    if not SetParameter(nPortNo, iSlaveNo):
        print("Failed to set parameter.")

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
