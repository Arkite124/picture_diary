# day5_self1.py
import json
from pathlib import Path

from ab_test import compute_p95, run_ab_test


BASE_DIR = Path(__file__).parent
DOMAIN_NAME = "travel"
N_CALLS = 3


def main() -> None:
    # Step 1. 도메인 프롬프트 JSON 로드
    domain_path = BASE_DIR / "domains" / f"{DOMAIN_NAME}_prompts.json"

    with open(domain_path, "r", encoding="utf-8") as f:
        domain_data = json.load(f)

    scenes = domain_data["scenes"]

    # 사용할 장면 1개 선택
    scene = scenes[0]

    diary_sentence = scene["diary_sentence"]
    prompt_addons = scene["prompt_addons"]

    # diary_sentence와 prompt_addons를 합쳐 prompt 생성
    prompt = diary_sentence + ", " + ", ".join(prompt_addons)

    print("[선택 도메인]", DOMAIN_NAME)
    print("[사용 장면]", scene["id"])
    print("[프롬프트]", prompt)

    # Step 2. A/B 실행 + P95 계산
    ab_result = run_ab_test(prompt, n_calls=N_CALLS)

    a_latencies = ab_result["a_latencies"]
    b_latencies = ab_result["b_latencies"]

    p95_a = compute_p95(a_latencies)
    p95_b = compute_p95(b_latencies)

    print(f"A P95: {p95_a:.2f}초")
    print(f"B P95: {p95_b:.2f}초")

    # Step 3. ab_test_results.json 저장
    result_path = BASE_DIR / "ab_test_results.json"

    result_data = {
        "domain": DOMAIN_NAME,
        "prompt": prompt,
        "seed": {
            "A": ab_result["a_seed"],
            "B": ab_result["b_seed"]
        },
        "latencies": {
            "A": a_latencies,
            "B": b_latencies
        },
        "p95": {
            "A": p95_a,
            "B": p95_b
        }
    }

    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    print("[저장 완료]", result_path)

    # Step 4. cost_report.md 작성
    report_path = BASE_DIR / "cost_report.md"

    total_calls = N_CALLS * 2

    report = f"""# Day 5 비용 및 지연 시간 리포트

## 1. 5일 누적 비용 표

| Day | 작업 | 호출 수 | 예상 비용 |
|---|---:|---:|---:|
| Day 1 | 기본 프롬프트 실습 | 4 | ~$0.08 (gpt-image-1-mini ×4) |
| Day 2 | 이미지 생성 실습 | 1 | ~$0.003 (FLUX-schnell ×1) |
| Day 3 | 장면 추출 및 이미지 생성 | 5 | ~$0.04 (GPT-4o-mini ×1 + gpt-image-1-mini ×4) |
| Day 4 | 영상 생성 파이프라인 | 6 | ~$0.51 (Kling ×1 + FLUX ×4 + GPT-4o-mini ×1) |
| Day 5 | A/B 테스트 이미지 생성 | {total_calls} | 모델/요금표 기준 확인 필요 |

## 2. A/B 테스트 정보

| 항목 | 값 |
|---|---|
| 도메인 | {DOMAIN_NAME} |
| 사용 프롬프트 | {prompt} |
| A Seed | {ab_result["a_seed"]} |
| B Seed | {ab_result["b_seed"]} |
| A 호출 수 | {len(a_latencies)} |
| B 호출 수 | {len(b_latencies)} |

## 3. P95 지연 시간

| 그룹 | Latencies(sec) | P95(sec) |
|---|---|---:|
| A | {a_latencies} | {p95_a:.2f} |
| B | {b_latencies} | {p95_b:.2f} |

## 4. 간단 해석

A 그룹과 B 그룹은 같은 프롬프트를 사용하지만 seed가 다릅니다.  
P95는 평균이 아니라 느린 구간을 보는 값이므로, 실제 서비스 안정성을 확인할 때 참고할 수 있습니다.
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("[저장 완료]", report_path)


if __name__ == "__main__":
    main()
