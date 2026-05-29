# pipeline.py — 그림일기 통합 파이프라인
import json
import time
import requests
import fal_client

from datetime import date
from pathlib import Path

from agents.scene import extract_scenes      # Day 3 self1
from agents.image import batch_generate     # Day 3 self2
from agents.video import submit_kling, status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget


def picture_diary_pipeline(
    diary_text: str,
    model: str = "flux",
    animate_first: bool = True
) -> dict:
    """그림일기 통합 파이프라인. diary 텍스트 → scenes → images → (선택) 첫 장면 영상 → results.json."""

    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) scene 단계: diary_text → scenes
    scenes = extract_scenes(diary_text)

    print("[1단계 완료] scenes 추출")
    print(json.dumps(scenes, ensure_ascii=False, indent=2))

    # 2) image 단계: scenes → image_paths
    image_paths = batch_generate(scenes, model, out_dir)

    print("[2단계 완료] 이미지 생성")
    for path in image_paths:
        print(path)

    # 3) video 단계: image_paths[0] → scene_1.mp4
    video_path = None

    if animate_first and image_paths:
        print("[3단계 시작] 첫 번째 이미지 영상화")

        first_image_path = Path(image_paths[0])

        # fal.ai 임시 URL로 업로드
        image_url = fal_client.upload_file(str(first_image_path))

        video_prompt = "slow zoom in, gentle sway, soft light, calm cinematic motion"

        # Kling 작업 제출
        task_id = submit_kling(
            image_url=image_url,
            prompt=video_prompt,
            duration=5
        )

        print("Kling task_id:", task_id)

        iteration = 0
        start_ts = time.time()
        status = ""
        used_usd = 0.0

        while True:
            # 4종 가드 적용
            if not (
                check_max_iter(iteration)
                and check_timeout(start_ts)
                and check_budget(used_usd)
            ):
                print("[가드 발동] 영상 폴링 중단")
                break

            status = status_kling(task_id)

            if check_predicate(status):
                print("[완료] Kling 영상 생성 완료")
                break

            iteration += 1
            time.sleep(5)

        # 완료 상태면 결과 영상 다운로드
        if check_predicate(status):
            video_url = result_kling(task_id)

            video_path_obj = out_dir / "scene_1.mp4"

            response = requests.get(video_url)
            response.raise_for_status()

            with open(video_path_obj, "wb") as f:
                f.write(response.content)

            video_path = str(video_path_obj)
            print("[영상 저장 완료]", video_path)
        else:
            print("[영상 생성 실패 또는 중단]", status)

    # 4) results 단계: 전체 메타데이터 → results.json
    diary_first_line = diary_text.strip().splitlines()[0] if diary_text.strip() else ""

    results = {
        "diary_first_line": diary_first_line,
        "scenes": scenes,
        "images": [str(path) for path in image_paths],
        "video": video_path,
    }

    results_path = out_dir / "results.json"

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("[4단계 완료] results.json 저장")
    print(results_path)

    return results