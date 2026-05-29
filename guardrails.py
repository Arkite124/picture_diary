import time
from typing import Callable

MAX_ITER = 60
TIMEOUT_SEC = 300
BUDGET_CAP_USD = 0.50

def check_max_iter(iteration: int) -> bool:
    # iteration이 최대 반복 횟수보다 작으면 계속 진행
    return iteration < MAX_ITER

def check_timeout(start_ts: float) -> bool:
    # 시작 시간으로부터 TIMEOUT_SEC 초가 지나지 않았으면 계속 진행
    return time.time() - start_ts < TIMEOUT_SEC

def check_predicate(status: str, accept: tuple = ("completed", "succeeded")) -> bool:
    # 상태 문자열을 소문자로 바꾼 뒤 허용 상태에 포함되는지 확인
    return status.lower() in accept

def check_budget(used_usd: float) -> bool:
    # 사용 금액이 예산 상한보다 작으면 계속 진행
    return used_usd < BUDGET_CAP_USD