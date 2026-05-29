from pathlib import Path
import fal_client
import sys
from datetime import date
import time, requests
from pathlib import Path 
from agents.video import status_kling, result_kling 
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget

task_id = Path("kling_task_id.txt").read_text().strip()
print(f"self1에서 받은 task_id: {task_id}")

KLING_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"
# 여기에 fal_client.status(KLING_MODEL, task_id, with_logs=False)를 호출하고
# status 객체와 status 문자열을 출력하는 코드를 채워요.
task_id = Path("kling_task_id.txt").read_text().strip()

iteration = 0
start_ts = time.time()
status = ""
user_usd = 0.0

while True:
    # 4종 가드 적용
    if not (
        check_max_iter(iteration)
        and check_timeout(start_ts)
        and check_budget(user_usd)
    ):
        print("[가드 발동] 중단")
        break

    status = status_kling(task_id)
    print(f"[{iteration}] status: {status}")
    # print(type(status))
    # sys.exit()
    # 완료 상태 도달 시 중단
    # type(status).__name__ 을 써야만, Completed와 같은 상태가 정상적으로 인식
    # type(status)는 status가 받아오는 응답의 형태를 말해주고
    # <class 'fal_client.client.Completed'>
    # .__name__은 형태의 이름(<class 'fal_client.client.Completed'> -> Completed) 을 말해준다.
    # 그냥 status만 사용시 check_predicate 인자에 오류가 발생
    if check_predicate(type(status).__name__):
        print("[완료] Kling 영상 생성 완료")
        break

    iteration += 1
    time.sleep(5)  # 5초 간격 폴링

# 완료되었을 때 결과 영상 다운로드
if check_predicate(type(status).__name__):
    video_url = result_kling(task_id)
    today = date.today().isoformat()
    output_dir = Path("outputs") / today
    output_dir.mkdir(parents=True, exist_ok=True)

    video_path = output_dir / "scene_1.mp4"

    response = requests.get(video_url)
    response.raise_for_status()

    with open(video_path, "wb") as f:
        f.write(response.content)

    print(f"[저장 완료] {video_path}")
else:
    print(f"[실패 또는 중단] 최종 status: {type(status).__name__}")

from pipeline import picture_diary_pipeline
from pathlib import Path

diary_text = Path("diary.md").read_text(encoding="utf-8")
picture_diary_pipeline(diary_text, animate_first=False)