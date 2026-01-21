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

INCPOS = 200000
ABSPOS = 0


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


def PosIncOverride(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Move AxisIncPos & PositionIncOverride
    lIncPos = INCPOS
    lVelocity = 20000
    lActualPos = 0
    lChangePos = 0
    lPosDetect = 100000

    print("---------------------------")
    print("[Inc Mode] Move Motor Start!")

    # 1. Move Command
    # Move the motor by INCPOS(200000) [pulse]
    if FAS_MoveSingleAxisIncPos(nPortNo, iSlaveNo, lIncPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisIncPos) was failed.")
        return False

    # 2. Check Condition
    # Check current position
    while True:
        time.sleep(0.001)
        status_result, lActualPos = FAS_GetActualPos(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Funtion(FAS_GetActualPos) was failed.")
            return False
        if lActualPos > lPosDetect:
            break

    # 3. Change Position
    # If the current position is less than the target position, change final position.
    lChangePos += lIncPos
    if FAS_PositionIncOverride(nPortNo, iSlaveNo, lChangePos) != FMM_OK:
        print("Function(FAS_PositionIncOverride) was failed.")
        return False
    else:
        print(
            "[Before] Target Position : %d[pulse] / [After] Target Position : %d[pulse]"
            % (lIncPos, lChangePos + lIncPos)
        )
    # 4. Confirm Move Complete
    # Check the Axis status until motor stops and the Inposition value is checked
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False
        if not (axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING) and (
            axis_status & EZISERVO_AXISSTATUS.FFLAG_INPOSITION
        ):
            break

    return True


def PosAbsOvrride(nPortNo: int, iSlaveNo: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Move AxisAbsPos & PositionAbsOverride
    lVelocity = 40000
    lIncEndPos = 0
    lActualPos = 0
    lAbsPos = 0
    lChangePos = 0

    status_result, lIncEndPos = FAS_GetActualPos(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Function(FAS_GetActualPos) was failed.")
        return False

    print("---------------------------")

    # 1. Move Command
    # Move the motor by ((lIncEndPos)* 1/ 4) pulse (target position : Absolute position)
    lAbsPos = lIncEndPos // 4

    if FAS_MoveSingleAxisAbsPos(nPortNo, iSlaveNo, lAbsPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisAbsPos) was failed.")
        return False
    print("[ABS Mode] Move Motor Start!")

    # 2. Check Condition
    # Check current position
    while True:
        time.sleep(0.001)

        status, lActualPos = FAS_GetActualPos(nPortNo, iSlaveNo)
        if status != FMM_OK:
            print("Function(FAS_GetActualPos) was failed.")
            break

        if lActualPos < (lIncEndPos / 2):
            break

    # 3. Change Position
    # if the current position falls below half the INC End position, change the target position to zero.
    lChangePos = ABSPOS
    if FAS_PositionAbsOverride(nPortNo, iSlaveNo, lChangePos) != FMM_OK:
        print("Function(FAS_PositionAbsOverride) was failed.")
        return False
    else:
        print(
            "Before Target Position: %d[pulse] / Change Target Position: %d[pulse]"
            % (lAbsPos, lChangePos)
        )

    # 4. Confirm Move Complete
    # Check the Axis status until motor stops and the Inposition value is checked
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
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

    # Move AxisIncPos & PositionIncOverride
    if not PosIncOverride(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Move AxisAbsPos & PositionAbsOverride
    if not PosAbsOvrride(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
