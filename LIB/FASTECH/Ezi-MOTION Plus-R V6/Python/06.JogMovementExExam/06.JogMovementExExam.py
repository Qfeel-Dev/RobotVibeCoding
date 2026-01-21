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


def JogMove(nPortNo: int, iSlaveNo: int, nAccDecTime: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    nTargetVeloc = 10000
    nDirect = 1
    nSeconds = 3  # Wait 3 Sec

    # Set Jog Acc/Dec Time
    if FAS_SetParameter(nPortNo, iSlaveNo, SERVO_JOGACCDECTIME, nAccDecTime) != FMM_OK:
        print("Function(FAS_SetParameter) was failed.")
        return False

    print("---------------------------")
    if FAS_MoveVelocity(nPortNo, iSlaveNo, nTargetVeloc, nDirect) != FMM_OK:
        print("Function(FAS_MoveVelocity) was failed.")
        return False

    print("Move Motor(Jog Mode)!")
    time.sleep(nSeconds)

    if FAS_MoveStop(nPortNo, iSlaveNo) != FMM_OK:
        print("Function(FAS_MoveStop) was failed.")
        return False

    # Wait until FFLAG_MOTIONING is OFF
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING):
            print("Move Stop!")
            break

    return True


def JogExMove(nPortNo: int, iSlaveNo: int, nAccDecTime: int):

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # MoveVelocityEx

    # Set velocity
    nDirect = 1
    lVelocity = 30000
    nSeconds = 3  # Wait 3 Sec

    # set user setting bit(BIT_USE_CUSTOMACCDEC) and acel/decel time value
    opt = VELOCITY_OPTION_EX(BIT_USE_CUSTOMACCDEC=1, wCustomAccDecTime=nAccDecTime)

    print("-----------------------------------------------------------")
    if FAS_MoveVelocityEx(nPortNo, iSlaveNo, lVelocity, nDirect, opt) != FMM_OK:
        print("Function(FAS_MoveVelocityEx) was failed.")
        return False

    print("Move Motor(Jog Ex Mode)!")
    time.sleep(nSeconds)

    if FAS_MoveStop(nPortNo, iSlaveNo) != FMM_OK:
        print("Function(FAS_MoveStop) was failed.")
        return False

    # Wait until FFLAG_MOTIONING is OFF
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING):
            print("Move Stop!")
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

    # MoveVelocity with AccDecTime = 100
    if not JogMove(nPortNo, iSlaveNo, 100):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocity with AccDecTime = 200
    if not JogMove(nPortNo, iSlaveNo, 200):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocity with AccDecTime = 300
    if not JogMove(nPortNo, iSlaveNo, 300):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocityEx with AccDecTime = 100
    if not JogExMove(nPortNo, iSlaveNo, 100):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocityEx with AccDecTime = 200
    if not JogExMove(nPortNo, iSlaveNo, 200):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocityEx with AccDecTime = 300
    if not JogExMove(nPortNo, iSlaveNo, 300):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
