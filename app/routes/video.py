from fastapi import APIRouter
from app.services.gemini_service import generar_guion
from app.services.tts_service import generar_audios_desde_guion
from app.models.schemas import TopicRequest
from app.services.video_service import generate_video

router = APIRouter(prefix="/video", tags=["Video"])


@router.post("/generate-script")
def generate_script(data: TopicRequest):

    guion = generar_guion(data.topic)

    # Validación básica
    if not isinstance(guion, dict):
        return {
            "error": "El guion no es válido",
            "raw": guion
        }

    audios = generar_audios_desde_guion(guion)
    video = generate_video(guion, audios)

    return {
        "script": guion,
        "audio_files": audios,
    }