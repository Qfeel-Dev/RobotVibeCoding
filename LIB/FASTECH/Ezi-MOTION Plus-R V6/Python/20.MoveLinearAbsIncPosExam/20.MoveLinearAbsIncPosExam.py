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

SLAVE_CNT = 2

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
    # Check Drive's Error
    status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)

    if status_result != FMM_OK:
        print("[Slave : %d ] Function(FAS_GetAxisStatus) was failed." % iSlaveNo)
        return False

    if axis_status & EZISERVO_AXISSTATUS.FFLAG_ERRORALL:
        # if Drive's Error was detected, Reset the ServoAlarm
        if FAS_ServoAlarmReset(nPortNo, iSlaveNo) != FMM_OK:
            print("[Slave : %d ] Function(FAS_ServoAlarmReset) was failed." % iSlaveNo)
            return False

    return True


def SetServoOn(nPortNo: int, iSlaveNo: int) -> bool:
    # Check Drive's Servo Status
    status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)

    if status_result != FMM_OK:
        print("[Slave : %d ] Function(FAS_GetAxisStatus) was failed." % iSlaveNo)
        return False

    # if ServoOnFlagBit is OFF('0'), switch to ON('1')
    if (axis_status & EZISERVO_AXISSTATUS.FFLAG_SERVOON) == 0:
        if FAS_ServoEnable(nPortNo, iSlaveNo, 1) != FMM_OK:
            print("[Slave : %d ] Function(FAS_ServoEnable) was failed." % iSlaveNo)
            return False

        while (
            axis_status & EZISERVO_AXISSTATUS.FFLAG_SERVOON
        ) == 0:  # Wait until FFLAG_SERVOON is ON
            time.sleep(0.001)

            status_result, axis_status = FAS_GetAxisStatus(nPortNo, iSlaveNo)
            if status_result != FMM_OK:
                print("[Slave : %d ] Function(FAS_GetAxisStatus) was failed." % iSlaveNo)
                return False

            if (axis_status & EZISERVO_AXISSTATUS.FFLAG_SERVOON) != 0:
                print("[Slave : %d ] Servo ON" % iSlaveNo)

    else:
        print("[Slave : %d ] Servo is already ON" % iSlaveNo)

    return True


def MoveLinearIncPos(nPortNo: int, iSlaveNo: int) -> bool:
    # Move Linear IncPos
    lIncPos = [370000, 370000]
    wAccelTime = 100

    print("---------------------------")
    # Increase the motor by 370000 pulse (target position : Relative position)

    lVelocity = 40000

    print("[Linear Inc Mode] Move Motor!")

    if FAS_MoveLinearIncPos2(nPortNo, SLAVE_CNT, iSlaveNo, lVelocity, wAccelTime) != FMM_OK:
        print("Function(FAS_MoveLinearIncPos2) was failed.")
        return False
    # Check the Axis status until motor stops and the Inposition value is checked
    for nID in range(SLAVE_CNT):
        while True:
            time.sleep(0.001)
            status_result, axis_status = FAS_GetAxisStatus(nPortNo,nID)

            if status_result != FMM_OK:
                print("[Slave : %d ] Function(FAS_GetAxisStatus) was failed." % nID)
                return False

            if (
                not axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING
                and axis_status & EZISERVO_AXISSTATUS.FFLAG_INPOSITION
            ):
                break
    return True

def MoveLinearAbsPos(nPortNo: int, iSlaveNo: int) -> bool:

    # Move Linear AbsPos
    lAbsPos = [0, 0]
    wAccelTime = 100

    print("---------------------------")

    # Move the motor by 0 pulse (target position : Absolute position)
    lVelocity = 40000

    print("[Linear Abs Mode] Move Motor!")
    if FAS_MoveLinearAbsPos2(nPortNo, SLAVE_CNT, iSlaveNo, lAbsPos, lVelocity, wAccelTime) != FMM_OK:
        print("Function(FAS_MoveLinearAbsPos2) was failed.")
        return False

    # Check the Axis status until motor stops and the Inposition value is checked
    for nID in range(SLAVE_CNT):
        while True:
            time.sleep(0.001)
            status_result, axis_status = FAS_GetAxisStatus(nPortNo,nID)
            if status_result != FMM_OK:
                print("[Slave : %d ] Function(FAS_GetAxisStatus) was failed." % nID)
                return False

            if (
                not axis_status & EZISERVO_AXISSTATUS.FFLAG_MOTIONING
                and axis_status & EZISERVO_AXISSTATUS.FFLAG_INPOSITION
            ):
                break
    return True


def main():
    nPortNo = 11
    iSlaveNo = [2, 3]
    dwBaudRate = 115200
    
    # Device Connect
    if not Connect(nPortNo, dwBaudRate):
        input("Press Enter to exit...")
        exit(1)
    for nID in range(SLAVE_CNT):
        # Drive Error Check
        if not CheckDriveErr(nPortNo, iSlaveNo[nID]):
            input("Press Enter to exit...")
            sys.exit(1)

        # Servo On
        if not SetServoOn(nPortNo, iSlaveNo[nID]):
            input("Press Enter to exit...")
            sys.exit(1)

    # Move Linear IncPos
    if not MoveLinearIncPos(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        sys.exit(1)

    # Move Linear AbsPos
    if not MoveLinearAbsPos(nPortNo, iSlaveNo):
        input("Press Enter to exit...")
        sys.exit(1)

    # Connection Close
    FAS_Close(nPortNo)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()