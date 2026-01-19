#####################################################
# Version: 1.0.0                                    #
# Last modified date: 25.10.31                      #
# Changes log: First released version               #
#####################################################


# -*- coding: utf-8 -*-
from ctypes import *
import ctypes
from FAS_EziMOTIONPlusR_Internal import *
from MOTION_DEFINE import *


# ------------------------------------------------------------------------------
# 					Connection Functions
# ------------------------------------------------------------------------------
# def FAS_Connect(nPortNo: int, dwBaud: int) -> bool:
def FAS_Connect(nPortNo, dwBaud):
    return FAS_Connect_Original(ctypes.c_ubyte(nPortNo), ctypes.c_uint(dwBaud))


# def FAS_OpenPort(nPortNo: int, dwBaud: int) -> bool:
def FAS_OpenPort(nPortNo, dwBaud):
    return FAS_OpenPort_Original(ctypes.c_ubyte(nPortNo), ctypes.c_uint(dwBaud))


# def FAS_AttachSlave(nPortNo: int, iSlaveNo: int) -> bool:
def FAS_AttachSlave(nPortNo, iSlaveNo):
    return FAS_AttachSlave_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_Close(nPortNo: int):
def FAS_Close(nPortNo):
    FAS_Close_Original(ctypes.c_ubyte(nPortNo))


# def FAS_IsSlaveExist(nPortNo: int, iSlaveNo: int) -> bool:
def FAS_IsSlaveExist(nPortNo, iSlaveNo):
    return FAS_IsSlaveExist_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# ------------------------------------------------------------------------------
# 					Log Functions
# ------------------------------------------------------------------------------
# def FAS_EnableLog(bEnable: bool):
def FAS_EnableLog(bEnable):
    FAS_EnableLog_Original(ctypes.c_int(bEnable))


# def FAS_SetLogLevel(level: int):
def FAS_SetLogLevel(level):
    FAS_SetLogLevel_Original(ctypes.c_int(level))


# def FAS_SetLogPath(lpPath: str) -> bool:
def FAS_SetLogPath(lpPath):
    return FAS_SetLogPath_Original(to_unicode(lpPath))


# def FAS_PrintCustomLog(nPortNo: int, level: int, lpszMsg: str):
def FAS_PrintCustomLog(nPortNo, level, lpszMsg):
    FAS_PrintCustomLog_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_int(level), to_unicode(lpszMsg)
    )


# ------------------------------------------------------------------------------
# 					Info Functions
# ------------------------------------------------------------------------------
# def FAS_GetSlaveInfo(nPortNo: int, iSlaveNo: int) -> tuple[int, int, str]:
def FAS_GetSlaveInfo(nPortNo, iSlaveNo):
    pType = ctypes.c_ubyte()
    lpBuff = ctypes.create_string_buffer(256)

    result = FAS_GetSlaveInfo_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(pType),
        lpBuff,
        256
    )

    if result == 0:
        return result, pType.value, lpBuff.value.decode("utf-8")
    else:
        return result, None, None


# def FAS_GetMotorInfo(nPortNo: int, iSlaveNo: int) -> tuple[int, int, str]:
def FAS_GetMotorInfo(nPortNo, iSlaveNo):
    pType = ctypes.c_ubyte()
    lpBuff = ctypes.create_string_buffer(256)
    
    result = FAS_GetMotorInfo_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(pType),
        lpBuff,
        256
    )
    if result == 0:
        return result, pType.value, lpBuff.value.decode("utf-8")
    else:
        return result, None, None


# def FAS_GetSlaveInfoEx(nPortNo: int, iSlaveNo: int) -> tuple[int, str]:
def FAS_GetSlaveInfoEx(nPortNo, iSlaveNo):
    drive_info = CDrive_Info()
    result = FAS_GetSlaveInfoEx_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), byref(drive_info)
    )
    if result == 0:
        lpDriveInfo = CDrive_Info_to_Drive_Info(drive_info)
        return result, lpDriveInfo
    else:
        return result, None


# ------------------------------------------------------------------------------
# 					Parameter Functions
# ------------------------------------------------------------------------------
# def FAS_SaveAllParameters(nPortNo: int, iSlaveNo: int) -> int:
def FAS_SaveAllParameters(nPortNo, iSlaveNo):
    return FAS_SaveAllParameters_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )

#def FAS_SetParameter(nPortNo: int, iSlaveNo: int, iParamNo: int, lParamValue: int) -> int:
def FAS_SetParameter(nPortNo, iSlaveNo, iParamNo, lParamValue):
    return FAS_SetParameter_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(iParamNo),
        ctypes.c_int(lParamValue)
    )


# def FAS_GetParameter(nPortNo: int, iSlaveNo: int, iParamNo: int) -> tuple[int, int]:
def FAS_GetParameter(nPortNo, iSlaveNo, iParamNo):
    lParamValue = ctypes.c_int()
    result = FAS_GetParameter_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(iParamNo),
        ctypes.byref(lParamValue)
    )
    if result == 0:
        return result, lParamValue.value
    else:
        return result, None


# def FAS_GetROMParameter(nPortNo: int, iSlaveNo: int, iParamNo: int) -> tuple[int, int]:
def FAS_GetROMParameter(nPortNo, iSlaveNo, iParamNo):
    lRomParam = ctypes.c_int()
    result = FAS_GetROMParameter_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(iParamNo),
        ctypes.byref(lRomParam)
    )
    if result == 0:
        return result, lRomParam.value
    else:
        return result, None


# ------------------------------------------------------------------------------
# 					IO Functions
# ------------------------------------------------------------------------------
# def FAS_SetIOInput(nPortNo: int, iSlaveNo: int, dwIOSETMask: int, dwIOCLRMask: int) -> int:
def FAS_SetIOInput(nPortNo, iSlaveNo, dwIOSETMask, dwIOCLRMask):
    return FAS_SetIOInput_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(dwIOSETMask),
        ctypes.c_uint(dwIOCLRMask)
    )


# def FAS_GetIOInput(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetIOInput(nPortNo, iSlaveNo):
    dwIOInput = ctypes.c_uint()
    result = FAS_GetIOInput_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(dwIOInput)
    )
    if result == 0:
        return result, dwIOInput.value
    else:
        return result, None

# def FAS_SetIOOutput(nPortNo: int, iSlaveNo: int, dwIOSETMask: int, dwIOCLRMask: int) -> int: 
def FAS_SetIOOutput(nPortNo, iSlaveNo, dwIOSETMask, dwIOCLRMask):
    return FAS_SetIOOutput_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(dwIOSETMask),
        ctypes.c_uint(dwIOCLRMask)
    )


# def FAS_GetIOOutput(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetIOOutput(nPortNo, iSlaveNo):
    dwIOOutput = ctypes.c_uint()
    result = FAS_GetIOOutput_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(dwIOOutput)
    )
    if result == 0:
        return result, dwIOOutput.value
    else:
        return result, None

# def FAS_GetIOAssignMap(nPortNo: int, iSlaveNo: int, iIOPinNo: int) -> tuple[int, int, int]:
def FAS_GetIOAssignMap(nPortNo, iSlaveNo, iIOPinNo):
    dwIOLogicMask = ctypes.c_uint()
    bLevel = ctypes.c_ubyte()
    result = FAS_GetIOAssignMap_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(iIOPinNo),
        ctypes.byref(dwIOLogicMask),
        ctypes.byref(bLevel)
    )
    if result == 0:
        return result, dwIOLogicMask.value, bLevel.value
    else:
        return result, None, None

# def FAS_SetIOAssignMap(nPortNo: int, iSlaveNo: int, iIOPinNo: int, dwIOLogicMask: int, bLevel: int) -> int:
def FAS_SetIOAssignMap(nPortNo, iSlaveNo, iIOPinNo, dwIOLogicMask, bLevel):
    return FAS_SetIOAssignMap_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(iIOPinNo),
        ctypes.c_uint(dwIOLogicMask),
        ctypes.c_ubyte(bLevel)
    )


# def FAS_IOAssignMapReadROM(nPortNo: int, iSlaveNo: int) -> int:
def FAS_IOAssignMapReadROM(nPortNo, iSlaveNo):
    return FAS_IOAssignMapReadROM_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )


# ------------------------------------------------------------------------------
# 					Servo Driver Control Functions
# ------------------------------------------------------------------------------
# def FAS_ServoEnable(nPortNo: int, iSlaveNo: int, bOnOff: int) -> int:
def FAS_ServoEnable(nPortNo, iSlaveNo, bOnOff):
    return FAS_ServoEnable_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(bOnOff)
    )


# def FAS_ServoAlarmReset(nPortNo: int, iSlaveNo: int) -> int:
def FAS_ServoAlarmReset(nPortNo, iSlaveNo):
    return FAS_ServoAlarmReset_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )


# def FAS_StepAlarmReset(nPortNo: int, iSlaveNo: int, bReset: bool) -> int:
def FAS_StepAlarmReset(nPortNo, iSlaveNo, bReset):
    return FAS_StepAlarmReset_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(bReset)
    )


# def FAS_BrakeSet(nPortNo: int, iSlaveNo: int, bSet: int) -> tuple[int, int]:
def FAS_BrakeSet(nPortNo, iSlaveNo, bSet):
    nResult = ctypes.c_int()
    result = FAS_BrakeSet_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(bSet),
        ctypes.byref(nResult)
    )
    if result == 0:
        return result, nResult.value
    else:
        return result, None


# ------------------------------------------------------------------------------
# 					Read Status and Position
# ------------------------------------------------------------------------------
# def FAS_GetAxisStatus(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetAxisStatus(nPortNo, iSlaveNo):
    dwAxisStatus = ctypes.c_uint()
    result = FAS_GetAxisStatus_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(dwAxisStatus)
    )
    if result == 0:
        return result, dwAxisStatus.value
    else:
        return result, None


# def FAS_GetIOAxisStatus(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int, int]:
def FAS_GetIOAxisStatus(nPortNo, iSlaveNo):
    dwInStatus = ctypes.c_uint()
    dwOutStatus = ctypes.c_uint()
    dwAxisStatus = ctypes.c_uint()

    result = FAS_GetIOAxisStatus_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(dwInStatus),
        ctypes.byref(dwOutStatus),
        ctypes.byref(dwAxisStatus)
    )
    if result == 0:
        return result, dwInStatus.value, dwOutStatus.value, dwAxisStatus.value
    else:
        return result, None, None, None

# def FAS_GetMotionStatus(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int, int, int, int]:
def FAS_GetMotionStatus(nPortNo, iSlaveNo):
    lCmdPos = ctypes.c_int()
    lActPos = ctypes.c_int()
    lPosErr = ctypes.c_int()
    lActVel = ctypes.c_int()
    wPosItemNo = ctypes.c_ushort()

    result = FAS_GetMotionStatus_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(lCmdPos),
        ctypes.byref(lActPos),
        ctypes.byref(lPosErr),
        ctypes.byref(lActVel),
        ctypes.byref(wPosItemNo)
    )
    if result == 0:
        return (
            result,
            lCmdPos.value,
            lActPos.value,
            lPosErr.value,
            lActVel.value,
            wPosItemNo.value
        )
    else:
        return result, None, None, None, None, None

# def FAS_GetAllStatus(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int, int, int, int, int, int, int]:
def FAS_GetAllStatus(nPortNo, iSlaveNo):
    dwInStatus = ctypes.c_uint()
    dwOutStatus = ctypes.c_uint()
    dwAxisStatus = ctypes.c_uint()
    lCmdPos = ctypes.c_int()
    lActPos = ctypes.c_int()
    lPosErr = ctypes.c_int()
    lActVel = ctypes.c_int()
    wPosItemNo = ctypes.c_ushort()

    result = FAS_GetAllStatus_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(dwInStatus),
        ctypes.byref(dwOutStatus),
        ctypes.byref(dwAxisStatus),
        ctypes.byref(lCmdPos),
        ctypes.byref(lActPos),
        ctypes.byref(lPosErr),
        ctypes.byref(lActVel),
        ctypes.byref(wPosItemNo)
    )
    if result == 0:
        return (
            result,
            dwInStatus.value,
            dwOutStatus.value,
            dwAxisStatus.value,
            lCmdPos.value,
            lActPos.value,
            lPosErr.value,
            lActVel.value,
            wPosItemNo.value
        )
    else:
        return result, None, None, None, None, None, None, None, None

# def FAS_GetAllStatusEx(nPortNo: int, iSlaveNo: int, pTypes: list) -> tuple[int, list]:
def FAS_GetAllStatusEx(nPortNo, iSlaveNo, pTypes):
    pTypesarray = (ctypes.c_ubyte * len(pTypes))(*pTypes)
    pDatas = (ctypes.c_int * 12)()
    result = FAS_GetAllStatusEx_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        pTypesarray, ctypes.cast(pDatas, ctypes.POINTER(ctypes.c_int))
    )
    if result == 0:
        return result, list(pDatas)
    else:
        return result, None


# def FAS_SetCommandPos(nPortNo: int, iSlaveNo: int, lCmdPos: int) -> int:
def FAS_SetCommandPos(nPortNo, iSlaveNo, lCmdPos):
    return FAS_SetCommandPos_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(lCmdPos)
    )


# def FAS_SetActualPos(nPortNo: int, iSlaveNo: int, lActPos: int) -> int:
def FAS_SetActualPos(nPortNo, iSlaveNo, lActPos):
    return FAS_SetActualPos_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(lActPos)
    )


# def FAS_ClearPosition(nPortNo: int, iSlaveNo: int) -> int:
def FAS_ClearPosition(nPortNo, iSlaveNo):
    return FAS_ClearPosition_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_GetCommandPos(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetCommandPos(nPortNo, iSlaveNo):
    lCmdPos = ctypes.c_int()
    result = FAS_GetCommandPos_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(lCmdPos)
    )
    if result == 0:
        return result, lCmdPos.value
    else:
        return result, None


# def FAS_GetActualPos(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetActualPos(nPortNo, iSlaveNo):
    lActPos = ctypes.c_int()
    result = FAS_GetActualPos_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(lActPos)
    )
    if result == 0:
        return result, lActPos.value
    else:
        return result, None


# def FAS_GetPosError(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetPosError(nPortNo, iSlaveNo):
    lPosErr = ctypes.c_int()
    result = FAS_GetPosError_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(lPosErr)
    )
    if result == 0:
        return result, lPosErr.value
    else:
        return result, None


# def FAS_GetActualVel(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetActualVel(nPortNo, iSlaveNo):
    lActVel = ctypes.c_int()
    result = FAS_GetActualVel_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(lActVel)
    )
    if result == 0:
        return result, lActVel.value
    else:
        return result, None


# def FAS_GetAlarmType(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetAlarmType(nPortNo, iSlaveNo):
    nAlarmType = ctypes.c_ubyte()
    result = FAS_GetAlarmType_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(nAlarmType)
    )
    if result == 0:
        return result, nAlarmType.value
    else:
        return result, None


# ------------------------------------------------------------------
# 					Motion Functions.
# ------------------------------------------------------------------
# def FAS_MoveStop(nPortNo: int, iSlaveNo: int) -> int:
def FAS_MoveStop(nPortNo, iSlaveNo):
    return FAS_MoveStop_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_EmergencyStop(nPortNo: int, iSlaveNo: int) -> int:
def FAS_EmergencyStop(nPortNo, iSlaveNo):
    return FAS_EmergencyStop_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_MovePause(nPortNo: int, iSlaveNo: int, bPause: bool) -> int:
def FAS_MovePause(nPortNo, iSlaveNo, bPause):
    return FAS_MovePause_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(bPause)
    )


# def FAS_MoveOriginSingleAxis(nPortNo: int, iSlaveNo: int) -> int:
def FAS_MoveOriginSingleAxis(nPortNo, iSlaveNo):
    return FAS_MoveOriginSingleAxis_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )

# def FAS_MoveSingleAxisAbsPos(nPortNo: int, iSlaveNo: int, lAbsPos: int, lVelocity: int) -> int:
def FAS_MoveSingleAxisAbsPos(nPortNo, iSlaveNo, lAbsPos, lVelocity):
    return FAS_MoveSingleAxisAbsPos_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(lAbsPos),
        ctypes.c_uint(lVelocity)
    )

# def FAS_MoveSingleAxisIncPos(nPortNo: int, iSlaveNo: int, lIncPos: int, lVelocity: int) -> int:
def FAS_MoveSingleAxisIncPos(nPortNo, iSlaveNo, lIncPos, lVelocity):
    return FAS_MoveSingleAxisIncPos_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(lIncPos),
        ctypes.c_uint(lVelocity)
    )


# def FAS_MoveToLimit(nPortNo: int, iSlaveNo: int, lVelocity: int, iLimitDir: int) -> int:
def FAS_MoveToLimit(nPortNo, iSlaveNo, lVelocity, iLimitDir):
    return FAS_MoveToLimit_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(lVelocity),
        ctypes.c_int(iLimitDir)
    )


# def FAS_MoveVelocity(nPortNo: int, iSlaveNo: int, lVelocity: int, iVelDir: int) -> int:
def FAS_MoveVelocity(nPortNo, iSlaveNo, lVelocity, iVelDir):
    return FAS_MoveVelocity_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(lVelocity),
        ctypes.c_int(iVelDir)
    )


# def FAS_PositionAbsOverride(nPortNo: int, iSlaveNo: int, lOverridePos: int) -> int:
def FAS_PositionAbsOverride(nPortNo, iSlaveNo, lOverridePos):
    return FAS_PositionAbsOverride_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(lOverridePos)
    )


# def FAS_PositionIncOverride(nPortNo: int, iSlaveNo: int, lOverridePos: int) -> int:
def FAS_PositionIncOverride(nPortNo, iSlaveNo, lOverridePos):
    return FAS_PositionIncOverride_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_int(lOverridePos)
    )


# def FAS_VelocityOverride(nPortNo: int, iSlaveNo: int, lVelocity: int) -> int:
def FAS_VelocityOverride(nPortNo, iSlaveNo, lVelocity):
    return FAS_VelocityOverride_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_uint(lVelocity)
    )

# def FAS_MoveLinearAbsPos(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplAbsPos: list, lFeedrate: int, wAccelTime: int) -> int:
def FAS_MoveLinearAbsPos(nPortNo, nNoOfSlaves, iSlavesNo, lplAbsPos, lFeedrate, wAccelTime):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplAbsPosArray = (ctypes.c_int * nNoOfSlaves)(*lplAbsPos)
    result = FAS_MoveLinearAbsPos_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplAbsPosArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime)
    )
    return result

# def FAS_MoveLinearIncPos(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplIncPos: list, lFeedrate: int, wAccelTime: int) -> int:
def FAS_MoveLinearIncPos(nPortNo, nNoOfSlaves, iSlavesNo, lplIncPos, lFeedrate, wAccelTime):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplIncPosArray = (ctypes.c_int * nNoOfSlaves)(*lplIncPos)
    result = FAS_MoveLinearIncPos_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplIncPosArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime)
    )
    return result

# def FAS_MoveLinearAbsPos2(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplAbsPos: list, lFeedrate: int, wAccelTime: int) -> int:
def FAS_MoveLinearAbsPos2(nPortNo, nNoOfSlaves, iSlavesNo, lplAbsPos, lFeedrate, wAccelTime):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplAbsPosArray = (ctypes.c_int * nNoOfSlaves)(*lplAbsPos)
    result = FAS_MoveLinearAbsPos2_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplAbsPosArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime)
    )
    return result

# def FAS_MoveLinearIncPos2(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplIncPos: list, lFeedrate: int, wAccelTime: int) -> int:
def FAS_MoveLinearIncPos2(nPortNo, nNoOfSlaves, iSlavesNo, lplIncPos, lFeedrate, wAccelTime):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplIncPosArray = (ctypes.c_int * nNoOfSlaves)(*lplIncPos)
    result = FAS_MoveLinearIncPos2_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplIncPosArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime)
    )

    return result

# def FAS_MoveCircleAbsPos1(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplCirEndAbs: list, lplCirCenterAbs: list, iDirection: int, lFeedrate: int, wAccelTime: int, bSCurve: int) -> int:
def FAS_MoveCircleAbsPos1(
    nPortNo,
    nNoOfSlaves,
    iSlavesNo,
    lplCirEndAbs,
    lplCirCenterAbs,
    iDirection,
    lFeedrate,
    wAccelTime,
    bSCurve
):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplCirEndAbsArray = (ctypes.c_int * nNoOfSlaves)(*lplCirEndAbs)
    lplCirCenterAbsArray = (ctypes.c_int * nNoOfSlaves)(*lplCirCenterAbs)
    result = FAS_MoveCircleAbsPos1_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplCirEndAbsArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.cast(lplCirCenterAbsArray,ctypes.POINTER(ctypes.c_int)),
        ctypes.c_int(iDirection),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime),
        ctypes.c_int(bSCurve)
    )
    return result

# def FAS_MoveCircleIncPos1(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplCirEndInc: list, lplCirCenterInc: list, iDirection: int, lFeedrate: int, wAccelTime: int, bSCurve: int) -> int:
def FAS_MoveCircleIncPos1(
    nPortNo,
    nNoOfSlaves,
    iSlavesNo,
    lplCirEndInc,
    lplCirCenterInc,
    iDirection,
    lFeedrate,
    wAccelTime,
    bSCurve
):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplCirEndIncArray = (ctypes.c_int * nNoOfSlaves)(*lplCirEndInc)
    lplCirCenterIncArray = (ctypes.c_int * nNoOfSlaves)(*lplCirCenterInc)
    result = FAS_MoveCircleIncPos1_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplCirEndIncArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.cast(lplCirCenterIncArray,ctypes.POINTER(ctypes.c_int)),
        ctypes.c_int(iDirection),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime),
        ctypes.c_int(bSCurve)
    )
    return result

# def FAS_MoveCircleAbsPos2(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplCirEndAbs: list, lRadius: int, iDirection: int, lFeedrate: int, wAccelTime: int, bSCurve: int) -> int:
def FAS_MoveCircleAbsPos2(
    nPortNo,
    nNoOfSlaves,
    iSlavesNo,
    lplCirEndAbs,
    lRadius,
    iDirection,
    lFeedrate,
    wAccelTime,
    bSCurve
):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplCirEndAbsArray = (ctypes.c_int * nNoOfSlaves)(*lplCirEndAbs)
    result = FAS_MoveCircleAbsPos2_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplCirEndAbsArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(lRadius),
        ctypes.c_int(iDirection),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime),
        ctypes.c_int(bSCurve)
    )
    return result

# def FAS_MoveCircleIncPos2(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplCirEndInc: list, lRadius: int, iDirection: int, lFeedrate: int, wAccelTime: int, bSCurve: int) -> int:
def FAS_MoveCircleIncPos2(
    nPortNo,
    nNoOfSlaves,
    iSlavesNo,
    lplCirEndInc,
    lRadius,
    iDirection,
    lFeedrate,
    wAccelTime,
    bSCurve
):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplCirEndIncArray = (ctypes.c_int * nNoOfSlaves)(*lplCirEndInc)
    result = FAS_MoveCircleIncPos2_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplCirEndIncArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(lRadius),
        ctypes.c_int(iDirection),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime),
        ctypes.c_int(bSCurve)
    )
    return result

# def FAS_MoveCircleAbsPos3(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplCirCenterAbs: list, nAngle: int, iDirection: int, lFeedrate: int, wAccelTime: int, bSCurve: int) -> int:
def FAS_MoveCircleAbsPos3(
    nPortNo,
    nNoOfSlaves,
    iSlavesNo,
    lplCirCenterAbs,
    nAngle,
    iDirection,
    lFeedrate,
    wAccelTime,
    bSCurve
):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplCirCenterAbsArray = (ctypes.c_int * nNoOfSlaves)(*lplCirCenterAbs)
    result = FAS_MoveCircleAbsPos3_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplCirCenterAbsArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(nAngle),
        ctypes.c_int(iDirection),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime),
        ctypes.c_int(bSCurve)
    )
    return result

# def FAS_MoveCircleIncPos3(nPortNo: int, nNoOfSlaves: int, iSlavesNo: list, lplCirCenterInc: list, nAngle: int, iDirection: int, lFeedrate: int, wAccelTime: int, bSCurve: int) -> int:
def FAS_MoveCircleIncPos3(
    nPortNo,
    nNoOfSlaves,
    iSlavesNo,
    lplCirCenterInc,
    nAngle,
    iDirection,
    lFeedrate,
    wAccelTime,
    bSCurve
):
    iSlavesNoArray = (ctypes.c_ubyte * nNoOfSlaves)(*iSlavesNo)
    lplCirCenterAbsArray = (ctypes.c_int * nNoOfSlaves)(*lplCirCenterInc)
    result = FAS_MoveCircleIncPos3_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(nNoOfSlaves),
        ctypes.cast(iSlavesNoArray, ctypes.POINTER(ctypes.c_ubyte)),
        ctypes.cast(lplCirCenterAbsArray, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_uint(nAngle),
        ctypes.c_int(iDirection),
        ctypes.c_uint(lFeedrate),
        ctypes.c_ushort(wAccelTime),
        ctypes.c_int(bSCurve)
    )
    return result

# def FAS_TriggerOutput_RunA(nPortNo: int, iSlaveNo: int, bStartTrigger: int, lStartPos: int, dwPeriod: int, dwPulseTime: int) -> int:
def FAS_TriggerOutput_RunA(
    nPortNo,
    iSlaveNo,
    bStartTrigger,
    lStartPos,
    dwPeriod,
    dwPulseTime
):
    return FAS_TriggerOutput_RunA_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(bStartTrigger),
        ctypes.c_int(lStartPos),
        ctypes.c_uint(dwPeriod),
        ctypes.c_uint(dwPulseTime)
    )


# def FAS_TriggerOutput_Status(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_TriggerOutput_Status(nPortNo, iSlaveNo):
    bTriggerStatus = ctypes.c_ubyte()
    result = FAS_TriggerOutput_Status_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(bTriggerStatus)
    )
    if result == 0:
        return result, bTriggerStatus.value
    else:
        return result, None

# def FAS_SetTriggerOutputEx(nPortNo: int, iSlaveNo: int, nOutputNo: int, bRun: int, wOnTime: int, nTriggerCount: int, arrTriggerPosition: list) -> int:
def FAS_SetTriggerOutputEx(
    nPortNo,
    iSlaveNo,
    nOutputNo,
    bRun,
    wOnTime,
    nTriggerCount,
    arrTriggerPosition,
):
    arrType = (ctypes.c_int * nTriggerCount)(*arrTriggerPosition)
    result = FAS_SetTriggerOutputEx_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(nOutputNo),
        ctypes.c_ubyte(bRun),
        ctypes.c_ushort(wOnTime),
        ctypes.c_ubyte(nTriggerCount),
        ctypes.cast(arrType, ctypes.POINTER(ctypes.c_int))
    )

    return result

# def FAS_GetTriggerOutputEx(nPortNo: int, iSlaveNo: int, nOutputNo: int) -> tuple[int, int, int, int, List]:
def FAS_GetTriggerOutputEx(nPortNo, iSlaveNo, nOutputNo):
    bRun = ctypes.c_ubyte()
    wOnTime = ctypes.c_ushort()
    nTriggerCount = ctypes.c_ubyte()
    arrTriggerPosition = ctypes.c_int()
    result = FAS_GetTriggerOutputEx_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(nOutputNo),
        ctypes.byref(bRun),
        ctypes.byref(wOnTime),
        ctypes.byref(nTriggerCount),
        ctypes.byref(arrTriggerPosition)
    )
    if result == 0:
        return (
            result,
            bRun.value,
            wOnTime.value,
            nTriggerCount.value,
            list(arrTriggerPosition)
        )
    else:
        return result, None, None, None, None

# def FAS_MovePush(nPortNo: int,iSlaveNo: int,dwStartSpd: int,dwMoveSpd: int,lPosition: int,wAccel: int,wDecel: int,wPushRate: int,dwPushSpd: int,lEndPosition: int,wPushMode: int) -> int:
def FAS_MovePush(
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
):
    return FAS_MovePush_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(dwStartSpd),
        ctypes.c_uint(dwMoveSpd),
        ctypes.c_int(lPosition),
        ctypes.c_ushort(wAccel),
        ctypes.c_ushort(wDecel),
        ctypes.c_ushort(wPushRate),
        ctypes.c_uint(dwPushSpd),
        ctypes.c_int(lEndPosition),
        ctypes.c_ushort(wPushMode)
    )


# def FAS_GetPushStatus(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetPushStatus(nPortNo, iSlaveNo):
    nPushStatus = ctypes.c_ubyte()
    result = FAS_GetPushStatus_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(nPushStatus)
    )
    if result == 0:
        return result, nPushStatus.value
    else:
        return result, None

# ------------------------------------------------------------------
# 					Ex-Motion Functions.
# ------------------------------------------------------------------
# def FAS_MoveSingleAxisAbsPosEx(nPortNo: int, iSlaveNo: int, lAbsPos: int, lVelocity: int, lpExOption: MOTION_OPTION_EX) -> int:
def FAS_MoveSingleAxisAbsPosEx(
    nPortNo,
    iSlaveNo,
    lAbsPos,
    lVelocity,
    lpExOption
):

    opt = MOTION_OPTION_EX_to_CMOTION_OPTION_EX(lpExOption)
    result = FAS_MoveSingleAxisAbsPosEx_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(lAbsPos),
        ctypes.c_uint(lVelocity),
        ctypes.byref(opt)
    )
    return result

# def FAS_MoveSingleAxisIncPosEx(nPortNo: int, iSlaveNo: int, lIncPos: int, lVelocity: int, lpExOption: MOTION_OPTION_EX) -> int:
def FAS_MoveSingleAxisIncPosEx(
    nPortNo,
    iSlaveNo,
    lIncPos,
    lVelocity,
    lpExOption
):
    opt = MOTION_OPTION_EX_to_CMOTION_OPTION_EX(lpExOption)
    result = FAS_MoveSingleAxisIncPosEx_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(lIncPos),
        ctypes.c_uint(lVelocity),
        ctypes.byref(opt),
    )
    return result

# def FAS_MoveVelocityEx(nPortNo: int, iSlaveNo: int, lVelocity: int, iVelDir: int, lpExOption: VELOCITY_OPTION_EX) -> int:
def FAS_MoveVelocityEx(
    nPortNo,
    iSlaveNo,
    lVelocity,
    iVelDir,
    lpExOption
):
    opt = VELOCITY_OPTION_EX_to_CVELOCITY_OPTION_EX(lpExOption)
    result = FAS_MoveVelocityEx_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(lVelocity),
        ctypes.c_int(iVelDir),
        ctypes.byref(opt)
    )
    return result


# ------------------------------------------------------------------
# 					All-Motion Functions.
# ------------------------------------------------------------------
# def FAS_AllMoveStop(nPortNo: int) -> int:
def FAS_AllMoveStop(nPortNo):
    return FAS_AllMoveStop_Original(ctypes.c_ubyte(nPortNo))


# def FAS_AllEmergencyStop(nPortNo: int) -> int:
def FAS_AllEmergencyStop(nPortNo):
    return FAS_AllEmergencyStop_Original(ctypes.c_ubyte(nPortNo))


# def FAS_AllMoveOriginSingleAxis(nPortNo: int) -> int:
def FAS_AllMoveOriginSingleAxis(nPortNo):
    return FAS_AllMoveOriginSingleAxis_Original(ctypes.c_ubyte(nPortNo))


# def FAS_AllMoveSingleAxisAbsPos(nPortNo: int, lAbsPos: int, lVelocity: int) -> int:
def FAS_AllMoveSingleAxisAbsPos(nPortNo, lAbsPos, lVelocity):
    return FAS_AllMoveSingleAxisAbsPos_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_int(lAbsPos), ctypes.c_uint(lVelocity)
    )


# def FAS_AllMoveSingleAxisIncPos(nPortNo: int, lIncPos: int, lVelocity: int) -> int:
def FAS_AllMoveSingleAxisIncPos(nPortNo, lIncPos, lVelocity):
    return FAS_AllMoveSingleAxisIncPos_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_int(lIncPos), ctypes.c_uint(lVelocity)
    )


# ------------------------------------------------------------------
# 					Position Table Functions.
# ------------------------------------------------------------------
# def FAS_PosTableReadItem(nPortNo: int, iSlaveNo: int, wItemNo: int) -> tuple[int, List]:
def FAS_PosTableReadItem(nPortNo, iSlaveNo, wItemNo):
    Item = CITEM_NODE()
    result = FAS_PosTableReadItem_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ushort(wItemNo),
        byref(Item)
    )
    if result == 0:
        lpItem = CITEM_NODE_to_ITEM_NODE(Item)
        return result, lpItem
    else:
        return result, None

# def FAS_PosTableWriteItem(nPortNo: int, iSlaveNo: int, wItemNo: int, lpItem: ITEM_NODE) -> int:
def FAS_PosTableWriteItem(nPortNo, iSlaveNo, wItemNo, lpItem):
    Item = ITEM_NODE_to_CITEM_NODE(lpItem)
    result = FAS_PosTableWriteItem_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ushort(wItemNo),
        ctypes.byref(Item)
    )
    return result


# def FAS_PosTableWriteROM(nPortNo: int, iSlaveNo: int) -> int:
def FAS_PosTableWriteROM(nPortNo, iSlaveNo):
    return FAS_PosTableWriteROM_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_PosTableReadROM(nPortNo: int, iSlaveNo: int) -> int:
def FAS_PosTableReadROM(nPortNo, iSlaveNo):
    return FAS_PosTableReadROM_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )


# def FAS_PosTableRunItem(nPortNo: int, iSlaveNo: int, wItemNo: int) -> int:
def FAS_PosTableRunItem(nPortNo, iSlaveNo, wItemNo):
    return FAS_PosTableRunItem_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_ushort(wItemNo)
    )

# def FAS_PosTableReadOneItem(nPortNo: int, iSlaveNo: int, wItemNo: int, wOffset: int) -> tuple[int, int]:
def FAS_PosTableReadOneItem(nPortNo, iSlaveNo, wItemNo, wOffset):
    lPosItemVal = ctypes.c_int()
    result = FAS_PosTableReadOneItem_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ushort(wItemNo),
        ctypes.c_ushort(wOffset),
        ctypes.byref(lPosItemVal)
    )
    if result == 0:
        return result, lPosItemVal.value
    else:
        return result, None



# def FAS_PosTableWriteOneItem(nPortNo: int, iSlaveNo: int, wItemNo: int, wOffset: int, lPosItemVal: int) -> int:
def FAS_PosTableWriteOneItem(nPortNo, iSlaveNo, wItemNo, wOffset, lPosItemVal):
    return FAS_PosTableWriteOneItem_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ushort(wItemNo),
        ctypes.c_ushort(wOffset),
        ctypes.c_int(lPosItemVal)
    )

# def FAS_PosTableSingleRunItem(nPortNo: int, iSlaveNo: int, bNextMove: int, wItemNo: int) -> int:
def FAS_PosTableSingleRunItem(nPortNo, iSlaveNo, bNextMove, wItemNo):
    return FAS_PosTableSingleRunItem_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_int(bNextMove),
        ctypes.c_ushort(wItemNo)
    )


# ------------------------------------------------------------------
# 					Gap Control Functions.
# ------------------------------------------------------------------
# def FAS_GapControlEnable(nPortNo: int, iSlaveNo: int, wItemNo: int, lGapCompSpeed: int, lGapAccTime: int, lGapDecTime: int, lGapStartSpeed: int) -> int:
def FAS_GapControlEnable(
    nPortNo,
    iSlaveNo,
    wItemNo,
    lGapCompSpeed,
    lGapAccTime,
    lGapDecTime,
    lGapStartSpeed
):
    return FAS_GapControlEnable_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ushort(wItemNo),
        ctypes.c_int(lGapCompSpeed),
        ctypes.c_int(lGapAccTime),
        ctypes.c_int(lGapDecTime),
        ctypes.c_int(lGapStartSpeed)
    )


# def FAS_GapControlDisable(nPortNo: int, iSlaveNo: int) -> int:
def FAS_GapControlDisable(nPortNo, iSlaveNo):
    return FAS_GapControlDisable_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )


# def FAS_IsGapControlEnable(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int]:
def FAS_IsGapControlEnable(nPortNo, iSlaveNo):
    bIsEnable = ctypes.c_int()
    wCurrentItemNo = ctypes.c_ushort()
    result = FAS_IsGapControlEnable_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(bIsEnable),
        ctypes.byref(wCurrentItemNo)
    )
    if result == 0:
        return result, bIsEnable.value, wCurrentItemNo.value
    else:
        return result, None, None


# def FAS_GapControlGetADCValue(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GapControlGetADCValue(nPortNo, iSlaveNo):
    lADCValue = ctypes.c_int()
    result = FAS_GapControlGetADCValue_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(lADCValue)
    )
    if result == 0:
        return result, lADCValue.value
    else:
        return result, None

# def FAS_GapOneResultMonitor(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int, int, int, int, int, int]:
def FAS_GapOneResultMonitor(nPortNo, iSlaveNo):
    bUpdated = ctypes.c_ubyte()
    iIndex = ctypes.c_int()
    lGapValue = ctypes.c_int()
    lCmdPos = ctypes.c_int()
    lActPos = ctypes.c_int()
    lCompValue = ctypes.c_int()
    lReserved = ctypes.c_int()
    result = FAS_GapOneResultMonitor_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(bUpdated),
        ctypes.byref(iIndex),
        ctypes.byref(lGapValue),
        ctypes.byref(lCmdPos),
        ctypes.byref(lActPos),
        ctypes.byref(lCompValue),
        ctypes.byref(lReserved)
    )
    if result == 0:
        return (
            result,
            bUpdated.value,
            iIndex.value,
            lGapValue.value,
            lCmdPos.value,
            lActPos.value,
            lCompValue.value,
            lReserved.value
        )
    else:
        return result, None, None, None, None, None, None, None


# ------------------------------------------------------------------
# 					Alarm Type History Functions.
# ------------------------------------------------------------------
# def FAS_GetAlarmLogs(nPortNo: int, iSlaveNo: int) -> tuple[int, List]:
def FAS_GetAlarmLogs(nPortNo, iSlaveNo):
    AlarmLog = CALARM_LOG()
    result = FAS_GetAlarmLogs_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(AlarmLog)
    )
    if result == 0:
        pAlarmLog = CALARM_LOG_to_ALARM_LOG(AlarmLog)
        return result, pAlarmLog
    else:
        return result, None


# def FAS_ResetAlarmLogs(nPortNo: int, iS5laveNo: int) -> int:
def FAS_ResetAlarmLogs(nPortNo, iSlaveNo):
    return FAS_ResetAlarmLogs_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo)
    )


# ------------------------------------------------------------------
# 					I/O Module Functions.
# ------------------------------------------------------------------
# def FAS_GetInput(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int]:
def FAS_GetInput(nPortNo, iSlaveNo):
    uInput = ctypes.c_uint()
    uLatch = ctypes.c_uint()
    result = FAS_GetInput_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(uInput),
        ctypes.byref(uLatch)
    )
    if result == 0:
        return result, uInput.value, uLatch.value
    else:
        return result, None, None


# def FAS_ClearLatch(nPortNo: int, iSlaveNo: int, uLatchMask: int) -> int:
def FAS_ClearLatch(nPortNo, iSlaveNo, uLatchMask):
    return FAS_ClearLatch_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_uint(uLatchMask)
    )


# def FAS_GetLatchCount(nPortNo: int, iSlaveNo: int, iInputNo: int) -> tuple[int, int]:
def FAS_GetLatchCount(nPortNo, iSlaveNo, iInputNo):
    uCount = ctypes.c_uint()
    result = FAS_GetLatchCount_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(iInputNo),
        ctypes.byref(uCount)
    )
    if result == 0:
        return result, uCount.value
    else:
        return result, None


# def FAS_GetLatchCountAll(nPortNo: int, iSlaveNo: int) -> tuple[int, list]:
def FAS_GetLatchCountAll(nPortNo, iSlaveNo):
    ppuAllCount = (ctypes.c_uint * 16)()
    result = FAS_GetLatchCountAll_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(ppuAllCount)
    )
    if result == 0:
        return result, list(ppuAllCount)
    else:
        return result, None


# def FAS_GetLatchCountAll32(nPortNo: int, iSlaveNo: int) -> tuple[int, list]:
def FAS_GetLatchCountAll32(nPortNo, iSlaveNo):
    ppuAllCount = (ctypes.c_uint * 32)()
    result = FAS_GetLatchCountAll32_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(ppuAllCount)
    )
    if result == 0:
        return result, list(ppuAllCount)
    else:
        return result, None


# def FAS_ClearLatchCount(nPortNo: int, iSlaveNo: int, uInputMask: int) -> int:
def FAS_ClearLatchCount(nPortNo, iSlaveNo, uInputMask):
    return FAS_ClearLatchCount_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_uint(uInputMask)
    )


# def FAS_GetOutput(nPortNo: int, iSlaveNo: int) -> tuple[int, int, int]:
def FAS_GetOutput(nPortNo, iSlaveNo):
    uOutput = ctypes.c_uint()
    uStatus = ctypes.c_uint()
    result = FAS_GetOutput_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.byref(uOutput),
        ctypes.byref(uStatus)
    )
    if result == 0:
        return result, uOutput.value, uStatus.value
    else:
        return result, None, None


# def FAS_SetOutput(nPortNo: int, iSlaveNo: int, uSetMask: int, uClearMask: int) -> int:
def FAS_SetOutput(nPortNo, iSlaveNo, uSetMask, uClearMask):
    return FAS_SetOutput_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(uSetMask),
        ctypes.c_uint(uClearMask)
    )

# def FAS_SetTrigger(nPortNo: int, iSlaveNo: int, uOutputNo: int, pTrigger: TRIGGER_INFO) -> int:
def FAS_SetTrigger(nPortNo, iSlaveNo, uOutputNo, pTrigger):
    Trigger = TRIGGER_INFO_to_CTRIGGER_INFO(pTrigger)
    result = FAS_SetTrigger_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(uOutputNo),
        ctypes.byref(Trigger)
    )
    return result


# def FAS_SetRunStop(nPortNo: int, iSlaveNo: int, uRunMask: int, uStopMask: int) -> int:
def FAS_SetRunStop(nPortNo, iSlaveNo, uRunMask, uStopMask):
    return FAS_SetRunStop_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_uint(uRunMask),
        ctypes.c_uint(uStopMask)
    )


# def FAS_GetTriggerCount(nPortNo: int, iSlaveNo: int, uOutputNo: int) -> tuple[int, int]:
def FAS_GetTriggerCount(nPortNo, iSlaveNo, uOutputNo):
    uCount = ctypes.c_uint()
    result = FAS_GetTriggerCount_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(uOutputNo),
        ctypes.byref(uCount)
    )
    if result == 0:
        return result, uCount.value
    else:
        return result, None


# def FAS_GetIOLevel(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetIOLevel(nPortNo, iSlaveNo):
    uIOLevel = ctypes.c_uint()
    result = FAS_GetIOLevel_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(uIOLevel)
    )
    if result == 0:
        return result, uIOLevel.value
    else:
        return result, None


# def FAS_SetIOLevel(nPortNo: int, iSlaveNo: int, uIOLevel: int) -> int:
def FAS_SetIOLevel(nPortNo, iSlaveNo, uIOLevel):
    return FAS_SetIOLevel_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_uint(uIOLevel)
    )


# def FAS_LoadIOLevel(nPortNo: int, iSlaveNo: int) -> int:
def FAS_LoadIOLevel(nPortNo, iSlaveNo):
    return FAS_LoadIOLevel_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_SaveIOLevel(nPortNo: int, iSlaveNo: int) -> int:
def FAS_SaveIOLevel(nPortNo, iSlaveNo):
    return FAS_SaveIOLevel_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_GetInputFilter(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetInputFilter(nPortNo, iSlaveNo):
    filter = ctypes.c_ushort()
    result = FAS_GetInputFilter_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(filter)
    )
    if result == 0:
        return result, filter.value
    else:
        return result, None


# def FAS_SetInputFilter(nPortNo: int, iSlaveNo: int, filter: int) -> int:
def FAS_SetInputFilter(nPortNo, iSlaveNo, filter):
    return FAS_SetInputFilter_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ushort(filter)
    )


# def FAS_GetIODirection(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetIODirection(nPortNo, iSlaveNo):
    direction = ctypes.c_uint()
    result = FAS_GetIODirection_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(direction)
    )
    if result == 0:
        return result, direction.value
    else:
        return result, None


# def FAS_SetIODirection(nPortNo: int, iSlaveNo: int, direction: int) -> int:
def FAS_SetIODirection(nPortNo, iSlaveNo, direction):
    return FAS_SetIODirection_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.c_uint(direction)
    )


# ------------------------------------------------------------------
# 					Ezi-IO AD Functions
# ------------------------------------------------------------------
# def FAS_SetADConfig(nPortNo: int, iSlaveNo: int, channel: int, type: int, value: int) -> tuple[int,int]:
def FAS_SetADConfig(nPortNo, iSlaveNo, channel, type, value):
    recv = ctypes.c_int()
    result = FAS_SetADConfig_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(channel),
        ctypes.c_int(type),
        ctypes.c_int(value),
        ctypes.byref(recv))
    if result == 0:
        return result, recv.value
    else:
        return result, None

    

# def FAS_GetADConfig(nPortNo: int, iSlaveNo: int, channel: int, type: int) -> tuple[int, int]:
def FAS_GetADConfig(nPortNo, iSlaveNo, channel, type):
    value = ctypes.c_int()
    result = FAS_GetADConfig_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(channel),
        ctypes.c_int(type),
        ctypes.byref(value)
    )
    if result == 0:
        return result, value.value
    else:
        return result, None


# def FAS_LoadADConfig(nPortNo: int, iSlaveNo: int) -> int:
def FAS_LoadADConfig(nPortNo, iSlaveNo):
    return FAS_LoadADConfig_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_SaveADConfig(nPortNo: int, iSlaveNo: int) -> int:
def FAS_SaveADConfig(nPortNo, iSlaveNo):
    return FAS_SaveADConfig_Original(ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo))


# def FAS_ReadADValue(nPortNo: int, iSlaveNo: int, channel: int) -> tuple[int, int]:
def FAS_ReadADValue(nPortNo, iSlaveNo, channel):
    advalue = ctypes.c_short()
    result = FAS_ReadADValue_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(channel),
        ctypes.byref(advalue)
    )
    if result == 0:
        return result, advalue.value
    else:
        return result, None


# def FAS_ReadADAllValue(nPortNo: int, iSlaveNo: int, offset: int) -> tuple[int, list]:
def FAS_ReadADAllValue(nPortNo, iSlaveNo, offset):
    adbuffer = (ctypes.c_short * 8)()
    result = FAS_ReadADAllValue_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(offset),
        adbuffer
    )
    if result == 0:
        return result, list(adbuffer)
    else:
        return result, None


# def FAS_GetAllADResult(nPortNo: int, iSlaveNo: int) -> tuple[int, int]:
def FAS_GetAllADResult(nPortNo, iSlaveNo):
    result_array = AD_RESULT()
    result = FAS_GetAllADResult_Original(
        ctypes.c_ubyte(nPortNo), ctypes.c_ubyte(iSlaveNo), ctypes.byref(result_array)
    )
    if result == 0:
        return result, list(result_array.elements)
    else:
        return result, None

# def FAS_GetADResult(nPortNo: int, iSlaveNo: int, channel: int) -> tuple[int, float]:  
def FAS_GetADResult(nPortNo, iSlaveNo, channel):  
    adresult = ctypes.c_float()
    result = FAS_GetADResult_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(channel),
        ctypes.byref(adresult)
    )
    if result == 0:
        return result, adresult.value
    else:
        return result, None


# def FAS_SetADRange(nPortNo: int, iSlaveNo: int, channel: int, range: int) -> int:
def FAS_SetADRange(nPortNo, iSlaveNo, channel, range):
    return FAS_SetADRange_Original(
        ctypes.c_ubyte(nPortNo),
        ctypes.c_ubyte(iSlaveNo),
        ctypes.c_ubyte(channel),
        ctypes.c_int(range),
    )
