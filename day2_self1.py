from pathlib import Path
import re

seed = Path("scene_draft_seed.md")
if seed.exists():
    print(seed.read_text(encoding="utf-8")[:500])
else:
    print("scene_draft_seed.md 없음 — Day 1 self2 산출물을 확인하세요.")

REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]
def load_draft(path: Path) -> str:
    """scene_draft.md를 읽어 본문을 반환."""
    scene=path.read_text(encoding="utf-8")
    return scene

def count_scenes(text: str) -> int:
    """본문에서 '## 장면 N' 헤딩 수를 카운트."""
    # 여기에 re.findall + 길이 반환 코드를 채워요.
    # 힌트: 정규식 r'^## 장면 \d+' (re.M 플래그).
    scenes = re.findall(r'^## 장면 \d+', text, re.M)
    return len(scenes)

def check_fields(text: str, scene_idx: int) -> list[str]:
    """주어진 장면 인덱스에 빠진 필드 목록 반환. 모두 있으면 빈 리스트."""
    # 여기에 본문에서 '## 장면 {scene_idx}' 섹션을 잘라낸 후
    # REQUIRED_FIELDS 각각 'field:' 패턴이 있는지 검사하고 누락 목록을 반환하는 코드를 채워요.
    pattern = rf'^## 장면 {scene_idx}\b(.*?)(?=^## 장면 \d+|\Z)'
    match = re.search(pattern, text, re.M | re.S)
    if not match:
        return REQUIRED_FIELDS.copy()
    scene_text = match.group(1)
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        field_pattern = rf'^\s*-?\s*{re.escape(field)}\s*[:：]'
        if not re.search(field_pattern, scene_text, re.M):
            missing.append(field)
    return missing
if __name__ == "__main__":
    draft = load_draft(Path("scene_draft.md"))
    n = count_scenes(draft)
    print(f"[검출] 장면 수: {n}")
    for i in range(1, n + 1):
        missing = check_fields(draft, i)
        if missing:
            print(f"[누락] 장면 {i}: {', '.join(missing)}")
    print("[완료] 모든 장면 OK이면 self2로 진행하세요.")
