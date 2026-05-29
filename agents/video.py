import os
from dotenv import load_dotenv
import fal_client

load_dotenv()

KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video"  # 강사 day4-s3 시연 엔드포인트 일치

def submit_kling(image_url: str, prompt: str, duration: int = 5) -> str:
    # 여기에 fal_client.submit(KLING_MODEL, arguments={...})를 호출하고
    #   handler.request_id를 반환하는 코드를 채워요.
    # 힌트: arguments = {"image_url": image_url, "prompt": prompt, "duration": duration}
    # 힌트: submit은 즉시 반환하고 영상은 백그라운드에서 생성됩니다.
    arguments = {
        "image_url": image_url,
        "prompt": prompt,
        "duration": duration,
    }

    handler = fal_client.submit(
        KLING_MODEL,
        arguments=arguments,
    )

    return handler.request_id

def status_kling(request_id: str) -> str:
    """Kling status 1회 조회. 상태 문자열 반환."""
    status = fal_client.status(
        KLING_MODEL,
        request_id,
        with_logs=False,
    )

    return status


def result_kling(request_id: str) -> str:
    """Kling 완료된 영상 결과 받기. 영상 URL 반환."""
    result = fal_client.result(
        KLING_MODEL,
        request_id,
    )

    return result["video"]["url"]

