## 1. 주요 메서드 개별 예제 표

Fastech 라이브러리의 핵심 함수들을 Python에서 호출하는 예시입니다.

| 메서드명 | Python 활용 예시  | 설명 |
| :--- | :--- | :--- |
| **FAS_Connect** | `FAS_Connect(port_no, baud_rate)` | 지정된 COM 포트와 통신 속도로 연결을 시도합니다. |
| **FAS_Close** | `FAS_Close(port_no)` | 열려 있는 통신 포트를 닫고 자원을 해제합니다. |
| **FAS_ServoEnable** | `FAS_ServoEnable(port_no, slave_id, True)` | 모터의 자화(Magnetizing)를 시작하여 구동 가능 상태로 만듭니다. |
| **FAS_ServoAlarmReset** | `FAS_ServoAlarmReset(port_no, slave_id)` | 드라이버에 발생한 알람(에러) 상태를 해제합니다. |
| **FAS_GetAllStatus** | `FAS_GetAllStatus(port_no, id, byref(status))` | 입출력, 시스템 상태, 위치 등 모든 정보를 한 번에 읽어옵니다. |
| **FAS_MoveSingleAxisIncPos** | `FAS_MoveSingleAxisIncPos(port, id, 1000, 50000)` | 현재 위치 기준 지정한 펄스만큼 **상대 이동**합니다. |
| **FAS_MoveSingleAxisAbsPos** | `FAS_MoveSingleAxisAbsPos(port, id, 50000, 50000)` | 지정한 **절대 좌표** 위치로 이동합니다. |
| **FAS_MoveStop** | `FAS_MoveStop(port_no, slave_id)` | 구동 중인 모터를 설정된 감속 시간에 맞춰 **정지**시킵니다. |
| **FAS_EmergencyStop** | `FAS_EmergencyStop(port_no, slave_id)` | 감속 없이 모터를 **즉시 정지**시킵니다. |
| **FAS_MoveVelocity** | `FAS_MoveVelocity(port, id, 10000, 0)` | 지정된 속도로 무한 회전합니다. (0: CW, 1: CCW) |
| **FAS_MoveOriginSingleAxis** | `FAS_MoveOriginSingleAxis(port_no, slave_id)` | 파라미터에 정의된 시퀀스에 따라 **원점 복귀**를 수행합니다. |
| **FAS_SetParameter** | `FAS_SetParameter(port, id, 1, 500)` | 드라이버 내부 파라미터(가감속 등) 값을 변경합니다. |
| **FAS_GetParameter** | `FAS_GetParameter(port, id, 1, byref(val))` | 설정된 파라미터 값을 읽어옵니다. |
| **FAS_ClearPosition** | `FAS_ClearPosition(port_no, slave_id)` | 현재 모터의 위치 좌표를 0으로 초기화합니다. |
| **FAS_SetIOOutput** | `FAS_SetIOOutput(port, id, 0x01, 0x01)` | 드라이버의 디지털 출력 포트(Output)를 제어합니다. |

---

## 2. 설비용 제어 래핑 클래스 (Wrapper)

실무에서는 예외 처리와 상태 관리를 위해 아래와 같이 클래스화하여 사용합니다.

```python
import FAS_EziMotionPlusR as Ezi
from ctypes import *
import time

class EziServoManager:
    def __init__(self, port, baud, slave_id=0):
        self.port = port
        self.baud = baud
        self.slave_id = slave_id
        self.is_connected = False

    def connect(self):
        res = Ezi.FAS_Connect(self.port, self.baud)
        if res != 0:
            self.is_connected = True
            return True
        return False

    def initialize(self):
        """알람 리셋 및 서보 온"""
        if not self.is_connected: return False
        Ezi.FAS_ServoAlarmReset(self.port, self.slave_id)
        time.sleep(0.1)
        Ezi.FAS_ServoEnable(self.port, self.slave_id, True)
        return True

    def move_abs(self, position, velocity):
        """절대 좌표 이동 명령 후 즉시 리턴"""
        return Ezi.FAS_MoveSingleAxisAbsPos(self.port, self.slave_id, position, velocity)

    def is_moving(self):
        """현재 모터 구동 상태 확인"""
        dw_status = uint32_t(0)
        Ezi.FAS_GetStatus(self.port, self.slave_id, byref(dw_status))
        # 일반적으로 Bit 13이 Motion Moving 상태임 (매뉴얼 확인 권장)
        return bool(dw_status.value & 0x2000)

    def wait_move_done(self):
        """이동이 완료될 때까지 블로킹 대기"""
        while self.is_moving():
            time.sleep(0.05)
        return True

    def disconnect(self):
        if self.is_connected:
            Ezi.FAS_ServoEnable(self.port, self.slave_id, False)
            Ezi.FAS_Close(self.port)

    def move_inc(self, distance, velocity):
        """
        상대 좌표 이동 (Incremental Move)
        :param distance: 이동할 거리 (Pulse 단위, 양수/음수 가능)
        :param velocity: 이동 속도 (pps)
        """
        if not self.is_connected:
            print("[오류] 연결되지 않은 상태에서 이동 명령을 내릴 수 없습니다.")
            return Ezi.FMP_ERR_COMM_INVALID_PORT

        print(f"[MOVE] 현재 위치에서 {distance}만큼 상대 이동 시작 (속도: {velocity})")
        
        # FAS_MoveSingleAxisIncPos 호출
        res = Ezi.FAS_MoveSingleAxisIncPos(self.port, self.slave_id, distance, velocity)
        
        if res != Ezi.FMP_OK:
            print(f"[오류] 상대 이동 명령 실패: Code {res}")
        
        return res
```

## 3. 모션 제어 표준 로직

설비 SW 구동 시 권장되는 표준 로직 흐름입니다.

### [Step 1: 통신 및 하드웨어 초기화]
 1. FAS_Connect로 포트 점유.

 2. FAS_ServoAlarmReset을 호출하여 혹시 모를 드라이버 에러 해제.

 3. FAS_ServoEnable을 통해 모터 홀딩(Holding) 상태 진입.

### [Step 2: 원점 복귀 (Homing)]
 1. FAS_MoveOriginSingleAxis 실행.

 2. is_moving 체크를 통해 완료 대기.

 3. 원점 복귀 성공 시 FAS_ClearPosition으로 좌표계를 0으로 정렬.

### [Step 3: 운전 (Operation)]
 1. move_abs 또는 move_inc를 통해 모션 실행.

 2. 실행 중 FAS_GetAllStatus를 통해 상시적으로 HW Limit Sensor나 Alarm Bit가 발생하는지 인터록(Interlock) 감시.

### [Step 4: 예외 처리 (Error Handling)]
 1. 통신 에러: 리턴값이 FMP_OK가 아닐 경우 로그를 남기고 재시도(Retry) 로직 수행.

 2. 비상 정지: 센서 감지 혹은 사용자 중단 시 즉시 FAS_EmergencyStop 호출.

### [Step 5: 종료]
 1. 프로그램 종료 시 반드시 FAS_ServoEnable(False) 후 FAS_Close를 수행하여 통신 포트를 반환.