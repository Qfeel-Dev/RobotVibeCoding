# ConnectionExam

Notification before use
-------------------------------------------------------
Depending on the type of product you are using, the definitions of 'Parameter', 'IO Logic', 'AxisStatus', etc. may be different.
This example is based on 'Ezi-SERVO', so please apply the appropriate value depending on the product you are using.
```
Example)

FM_EZISERVO_PARAM			// Parameter enum when using 'Ezi-SERVO'	
FM_EZIMOTIONLINK_PARAM		// Parameter enum when using 'Ezi-MOTIONLINK'
```
[EN]    
This example code is implemented to run on Python 3.x and later.
If you use version 3.0 or less, you need to change the print and input functions.

[KR]  
이 예제코드는 파이썬 3.x이상에서 동작하도록 구현되어있습니다.
3.0이하 버전에서 사용하실경우 print, input함수의 변형이 필요합니다.

## 0. Program scenario
[EN]    		
1. Connect a device.
2. Get product information.
3. Close connection.

[KR]  
1. 장치 연결.
2. 제품 종류 확인.
3. 연결 해제.


## 1. Setting the Path
```python
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
```
[EN]    
This code adds the appropriate Library folder path according to the Python architecture to import FAS_EziMOTIONPlusE, MOTION_DEFINE, and ReturnCodes_Define modules.
If the Library folder is in a different path, enter that path in Library_path.

[KR]  
FAS_EziMOTIONPlusE, MOTION_DEFINE, ReturnCodes_Define 모듈들을 Import 하기 위하여 파이썬 아키텍쳐에 따라 알맞은 Library 폴더 경로를 추가하는 코드입니다.
Library 폴더가 다른 경로에 있는 경우, library_path에 해당 경로를 입력해 주시기 바랍니다.

## 2. Connect
``` python
nPortNo = 11
dwBaudRate = 115200

def Connect(nPortNo: int, dwBaudRate: int) -> bool:
    bSuccess = False

    if FAS_Connect(nPortNo, dwBaudRate) == False:
        print("Connection Fail!")
        bSuccess = False

    else:
        print("Conncetion Success!")
        bSuccess = True
    return bSuccess
```
[EN]    
'FAS_Connect' is a function for RS-485 connection through PortNo and BaudRate.
If the function returns 'TRUE', the connection is successful.

[KR]  
'FAS_Connect'는 PortNo와 BaudRate를 통해 RS-485 통신 연결을 하는 함수입니다.
함수가 'TRUE'를 리턴하면 연결이 성공한 것입니다.

## 3. Get product info
``` python
def CheckDriveInfo(nPortNo: int, iSlaveNo: int) -> bool:
    status_result, byType, version = FAS_GetSlaveInfo(nPortNo, iSlaveNo)

    if status_result != FMM_OK:
        print("Function(FAS_GetSlaveInfo) was failed.")
        return False
    print(
        "Port No %d / Slave No %d : TYPE= %d, Version= %s"
        % (nPortNo, iSlaveNo, byType, version)
    )
    return True
```
[EN]    
After successful connection, a function 'FAS_GetSlaveInfo' was used to check product information. 
This function is not required for connection, but to just show an example of using a function after successful connection.

[KR]  
연결 성공 후 제품의 정보를 확인하는 함수(FAS_GetSlaveInfo)를 사용하였습니다.
이 함수는 연결에 필요한 함수가 아닙니다. 연결 후 임의의 함수를 호출한 것입니다.

## 4. Connection close
``` python
 # Connection Close
 FAS_Close(nPortNo)
```
 [EN]    
Use 'FAS_Close' to close the connection.

[KR]  
'FAS_Close()'를 통해 연결을 해제할 수 있습니다.