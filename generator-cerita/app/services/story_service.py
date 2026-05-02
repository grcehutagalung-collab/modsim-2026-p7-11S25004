from app.extensions import SessionLocal
from app.models.story import Story
from app.models.story_request import StoryRequest
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

# Mapping panjang ke instruksi untuk LLM
LENGTH_MAP = {
    "pendek": "sekitar 150-200 kata",
    "sedang": "sekitar 300-400 kata",
    "panjang": "sekitar 500-700 kata",
}

def create_story(theme: str, genre: str, length: str):
    """
    Membuat satu cerita pendek berdasarkan tema, genre, dan panjang.
    Menyimpan StoryRequest dan Story ke database.
    Mengembalikan dict hasil.
    """
    length_desc = LENGTH_MAP.get(length, "sekitar 200 kata")

    prompt = (
        f"Buatlah sebuah cerita pendek dengan ketentuan berikut:\n"
        f"- Tema: {theme}\n"
        f"- Genre: {genre}\n"
        f"- Panjang cerita: {length_desc}\n\n"
        f"Kembalikan HANYA JSON dengan format berikut tanpa teks lain:\n"
        f'{{"title": "judul cerita", "content": "isi cerita lengkap"}}'
    )

    llm_result = generate_from_llm(prompt)
    parsed = parse_llm_response(llm_result)

    db = SessionLocal()
    try:
        # Simpan request log
        story_request = StoryRequest(theme=theme, genre=genre, length=length)
        db.add(story_request)
        db.flush()

        # Simpan cerita
        story = Story(
            title=parsed["title"],
            content=parsed["content"],
            request_id=story_request.id
        )
        db.add(story)
        db.commit()
        db.refresh(story)

        return {
            "id": story.id,
            "title": story.title,
            "content": story.content,
            "request_id": story.request_id,
            "created_at": story.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_all_stories(page: int = 1, per_page: int = 10):
    """
    Mengambil semua cerita dengan paginasi.
    """
    db = SessionLocal()
    try:
        total = db.query(Story).count()
        stories = (
            db.query(Story)
            .order_by(Story.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "stories": [
                {
                    "id": s.id,
                    "title": s.title,
                    "content": s.content,
                    "request_id": s.request_id,
                    "created_at": s.created_at.isoformat()
                }
                for s in stories
            ]
        }
    finally:
        db.close()


def delete_story(story_id: int):
    """
    Menghapus cerita berdasarkan ID.
    """
    db = SessionLocal()
    try:
        story = db.query(Story).filter(Story.id == story_id).first()
        if not story:
            return None
        db.delete(story)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
