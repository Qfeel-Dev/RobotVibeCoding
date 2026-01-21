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

CW = 1
CCW = 0


def Connect(nPortNo: int, dwBaudRate: int) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo, dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess


def CheckDriveErr(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check Drive's Error
    status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)

    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    if axis_status & EZISERVO_AXISSTATUS.FFLAG_ERRORALL:
        # if Drive's Error was detected, Reset the ServoAlarm
        if FAS_ServoAlarmReset(nPortNo, iSlaveNo) != FMM_OK:
            print("Function(FAS_ServoAlarmReset) was failed.")
            return False

    return True


def SetServoOn(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check Drive's Servo Status

    # if ServoOnFlagBit is OFF('0'), switch to ON('1')
    status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    if (axis_status & EZISERVO_AXISSTATUS.FFLAG_SERVOON) == 0:
        if FAS_ServoEnable(nPortNo, iSlaveNo, 1) != FMM_OK:
            print("Function(FAS_ServoEnable) was failed.")
            return False

        while (
            axis_status & EZISERVO_AXISSTATUS.FFLAG_SERVOON
        ) == 0:  # Wait until FFLAG_SERVOON is ON
            time.sleep(0.001)

            status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
            if status_result != FMM_OK:
                print("Function(FAS_GetAxisStatus) was failed.")
                return False

            if (axis_status & EZISERVO_AXISSTATUS.FFLAG_SERVOON) != 0:
                print("Servo ON")

    else:
        print("Servo is already ON")

    return True


def SetOriginParameter(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Set Origin Parameter
    nOrgSpeed = 50000
    nOrgSearchSpeed = 1000
    nOrgAccDecTime = 50
    nOrgMethod = (
        2  # Origin Method = 2 is 'Limit Origin' in the Ezi-SERVOII Plus-E model
    )
    nOrgDir = CW
    nOrgOffset = 0
    nOrgPositionSet = 0
    nOrgTorqueRatio = 50

    if FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGSPEED, nOrgSpeed) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO_ORGSPEED]) was failed.")
        return False

    if (
        FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGSEARCHSPEED, nOrgSearchSpeed)
        != FMM_OK
    ):
        print("Function(FAS_SetParameter[SERVO_ORGSEARCHSPEED]) was failed.")
        return False

    if (
        FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGACCDECTIME, nOrgAccDecTime)
        != FMM_OK
    ):
        print("Function(FAS_SetParameter[SERVO_ORGACCDECTIME]) was failed.")
        return False

    if FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGMETHOD, nOrgMethod) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO_ORGMETHOD]) was failed.")
        return False

    if FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGDIR, nOrgDir) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO_ORGDIR]) was failed.")
        return False

    if FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGOFFSET, nOrgOffset) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO_ORGOFFSET]) was failed.")
        return False

    if (
        FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGPOSITIONSET, nOrgPositionSet)
        != FMM_OK
    ):
        print("Function(FAS_SetParameter[SERVO_ORGPOSITIONSET]) was failed.")
        return False

    if (
        FAS_SetParameter(nPortNo, iSlaveNo, SERVO_ORGTORQUERATIO, nOrgTorqueRatio)
        != FMM_OK
    ):
        print("Function(FAS_SetParameter[SERVO_ORGTORQUERATIO]) was failed.")
        return False

    return True


def OriginSearch(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Act Origin Search Function
    print("---------------------------")

    # Origin Search Start
    if FAS_MoveOriginSingleAxis(nPortNo, iSlaveNo) != FMM_OK:
        print("Function(FAS_MoveOriginSingleAxis) was failed.")
        return False

    # Check the Axis status until OriginReturning value is released.

    while True:
        time.sleep(0.001)

        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO_AXISSTATUS.FFLAG_ORIGINRETURNING):
            break

    if axis_status & EZISERVO_AXISSTATUS.FFLAG_ORIGINRETOK:
        print("Origin Search Success!")
        return True
    else:
        print("Origin Search Fail!")
        return False


def main():
    nPortNo = 11
    iSlaveNo = 2
    dwBaudRate = 115200

    # Device Connect
    if not Connect(nPortNo, dwBaudRate):
        input("Press Enter to exit...")
        exit(1)

    # Drive Error Check
    if not CheckDriveErr(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # ServoOn
    if not SetServoOn(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Set Origin Parameter
    if not SetOriginParameter(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Act Origin Search Function
    if not OriginSearch(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
