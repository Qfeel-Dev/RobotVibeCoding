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


def OperatePushMode(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # normal position motion
    dwStartSpd = 1
    dwMoveSpd = 50000
    wAccel = 500
    wDecel = 500
    lPosition = 500000

    # push motion
    dwPushSpd = 2000
    wPushRate = 50
    wPushMode = 0  # Stop Mode Push
    lEndPosition = lPosition + 10000

    print("---------------------------")

    if (
        FAS_MovePush(
            nPortNo,
            iSlaveNo,
            dwStartSpd,
            dwMoveSpd,
            lPosition,
            wAccel,
            wDecel,
            wPushRate,
            dwPushSpd,
            lEndPosition,
            wPushMode
        )
        != FMM_OK
    ):
        print("Function(FAS_MovePush) was failed.")
        return False

    # Check the Axis status until motor stops and the FFLAG_MOTIONING value is released.

    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)

        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING):
            break
    return True


def CheckPushResult(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    dwOutPut = 0

    print("---------------------------")
    print("Check Result Function")

    status_result, dwOutput = FAS_GetIOOutput(nPortNo, iSlaveNo)

    if status_result != FMM_OK:
        print("Function(FAS_GetIOOutput) was failed.")
        return False
    else:
        if dwOutput & SERVO_OUT_LOGIC_RESERVED0:
            print("Work Detected!")
        else:
            print("Work Not Detected!")

    return True


def ReturnPosition(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Return Poisition

    # Move the motor by 0 pulse (target position : Absolute position)
    lAbsPos = 0
    lVelocity = 50000

    time.sleep(0.1)
    print("---------------------------")
    print("Return Position Start!")
    if FAS_MoveSingleAxisAbsPos(nPortNo, iSlaveNo, lAbsPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisAbsPos) was failed.")
        return False

    # Check the Axis status until motor stops and the Inposition value is checked

    while True:
        time.sleep(0.001)

        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Funtion(FAS_GetAxisStatus) was failed.")
            return False
        if not (axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING) and (
            axis_status & EZISERVO_AXISSTATUS.FFLAG_INPOSITION
        ):
            break

    return True


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

    # Operate PushMode
    if not OperatePushMode(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Check PushMotion Result
    if not CheckPushResult(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Return Position
    if not ReturnPosition(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
