from pathlib import Path
from agents.scene import extract_scenes, save_scenes, validate_scenes
# 여기에 diary.md를 읽는 코드를 채워요.
# 힌트: diary_text = Path("diary.md").read_text(encoding="utf-8")
# diary.md가 없으면 아래 예제 일기를 사용해도 돼요.
diary_text = " 버스 좌석에 앉아 벽에 기대어 졸면서 갔다. 열심히 컴퓨터 앞에 앉아 게임을 하고 있었다. 바다 속 돌고래들이 산호 위를 지나갔다. 저 멀리 갯바위에서 낚시하는 낚시꾼의 모습이 보인다."  # ← diary.md 내용을 여기에 채워요
# 장면 4가지를 생각하는 거라고 생각했는데 한가지를 깊게 생각하는 거 였어서 중간에 1번으로 통일했습니다.
print("[1] 장면 추출 중...")
scenes = extract_scenes(diary_text)
print(f"  → {len(scenes)}개 장면 추출 완료")
print("[2] 장면 검증 중...")
errors = validate_scenes(scenes)
if errors:
    for error in errors:
        print(f"  → 오류: {error}")
    exit(1)
else:
    print("  → 검증 통과")
print("[3] scene_extracted.json 저장 중...")
# 여기에 save_scenes(scenes, "scene_extracted.json") 호출 코드를 채워요.
save_scenes(scenes, "scene_extracted.json")
print("  → 저장 완료")
print("[완료] Day 3 self2의 agents/image.py에서 scene_extracted.json을 입력으로 사용할 수 있어요.")
