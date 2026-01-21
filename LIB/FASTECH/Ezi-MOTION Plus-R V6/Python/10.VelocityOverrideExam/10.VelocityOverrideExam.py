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

INCPOS = 200000 #IncMove Target Position

def Connect(nPortNo: int, dwBaudRate: int ) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo,dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess

def CheckDriveErr(nPortNo: int, iSlaveNo: int)-> bool:

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

def SetServoOn(nPortNo: int, iSlaveNo: int)-> bool:

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


def MovePosAndVelOverride(nPortNo: int, iSlaveNo: int)-> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

     # MoveSingleAxisIncPos & VelocityOverride

    # Move the motor by INCPOS(200000) [pulse]
    lIncPos = INCPOS
    lVelocity = 20000
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

    # 3. Change Velocity
    # If the current position is less than the target position, change velocity.
    lChangeVelocity = lVelocity * 2
    if FAS_VelocityOverride(nPortNo, iSlaveNo, lChangeVelocity) != FMM_OK:
        print("Function(FAS_VelocityOverride) was failed.")
        return False
    else:
        print(
            "Before Velocity : %d[pps] /Change Velocity : %d[pps]"
            % (lVelocity, lChangeVelocity)
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

def JogAndVelOverride(nPortNo: int, iSlaveNo: int)-> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # MoveVelocity & VelocityOverride

    lVelocity = 10000

    print("---------------------------")

    # 1. Move Command
    # Move the motor
    if FAS_MoveVelocity(nPortNo, iSlaveNo, lVelocity, CW) != FMM_OK:
        print("Funtion(FAS_MoveVelocuty) was failed.")
        return False
    else:
        print("Current Velocity : %d" % lVelocity)

    print(">> Wait... 3 Second")
    time.sleep(3)

    # 2. Change Velocity
    status_result, lActualVelocity = FAS_GetActualVel(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Funtion(FAS_GetActualVel) was failed")
        return False

    lChangeVelocity = lActualVelocity * 2
    if FAS_VelocityOverride(nPortNo, iSlaveNo, lChangeVelocity) != FMM_OK:
        print("Funtion(FAS_VelocityOverride) was failed")
        return False

    else:
        print(
            "Before Velocity : %d[pps] / Change Velocity : %d[pps]"
            % (lActualVelocity, lChangeVelocity)
        )

    print(">> Wait... 5 Second")
    time.sleep(5)

    # 3.Change Velocity
    status_result, lActualVelocity = FAS_GetActualVel(nPortNo, iSlaveNo)
    if status_result != FMM_OK:
        print("Funtion(FAS_GetActualVel) was failed")
        return False

    lChangeVelocity = lActualVelocity * 2
    if FAS_VelocityOverride(nPortNo, iSlaveNo, lChangeVelocity) != FMM_OK:
        print("Funtion(FAS_VelocityOverride) was failed")
        return False
    else:
        print(
            "Before Velocity : %d[pps] / Change Velocity : %d[pps]"
            % (lActualVelocity, lChangeVelocity)
        )

    print(">> Wait... 10 Second")
    time.sleep(10)

    # 4. Stop
    FAS_MoveStop(nPortNo, iSlaveNo)
    print("FAS_MoveStop!")
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

    # Move AxisIncPos & VelocityOverride
    if not MovePosAndVelOverride(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocity  & VelocityOverride
    if not JogAndVelOverride(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()