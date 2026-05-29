import time
import statistics

from agents.image import generate_image


def time_one_call(prompt: str, seed: int, model: str = "flux") -> float:
    """이미지 1회 호출에 걸린 시간을 초 단위로 돌려주는 함수."""
    start = time.perf_counter()

    generate_image(
        prompt=prompt,
        seed=seed,
        model=model
    )

    end = time.perf_counter()

    return end - start


def run_ab_test(prompt: str, n_calls: int = 3) -> dict:
    """같은 prompt를 seed A/B로 나누어 여러 번 호출하는 함수."""
    seed_a = 42
    seed_b = 137

    a_latencies = []
    b_latencies = []

    for i in range(n_calls):
        print(f"[A 그룹 {i + 1}/{n_calls}] seed={seed_a}")
        elapsed = time_one_call(prompt=prompt, seed=seed_a)
        a_latencies.append(elapsed)
        print(f"  걸린 시간: {elapsed:.2f}초")

    for i in range(n_calls):
        print(f"[B 그룹 {i + 1}/{n_calls}] seed={seed_b}")
        elapsed = time_one_call(prompt=prompt, seed=seed_b)
        b_latencies.append(elapsed)
        print(f"  걸린 시간: {elapsed:.2f}초")

    return {
        "a_seed": seed_a,
        "b_seed": seed_b,
        "a_latencies": a_latencies,
        "b_latencies": b_latencies
    }


def compute_p95(latencies: list[float]) -> float:
    """지연 시간 목록에서 P95 값을 계산하는 함수."""
    if not latencies:
        return 0.0

    sorted_latencies = sorted(latencies)

    # 95번째 백분위 위치 계산
    index = int(len(sorted_latencies) * 0.95) - 1

    # 인덱스가 음수나 범위 밖으로 나가지 않게 보정
    index = max(0, min(index, len(sorted_latencies) - 1))

    return sorted_latencies[index]