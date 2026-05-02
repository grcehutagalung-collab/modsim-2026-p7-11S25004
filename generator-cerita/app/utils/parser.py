import json
import re

def parse_llm_response(result):
    """
    Mengambil field 'response' dari hasil LLM,
    membersihkan markdown code fence, lalu parse JSON.
    Mengembalikan dict dengan key 'title' dan 'content'.
    """
    try:
        content = result.get("response") or result

        # Hapus markdown code fence: ```json ... ```
        content = re.sub(r"```json\s*|\s*```", "", content).strip()

        parsed = json.loads(content)
        return {
            "title": parsed.get("title", "Cerita Tanpa Judul"),
            "content": parsed.get("content", "")
        }

    except Exception as e:
        raise Exception(f"Invalid JSON from LLM: {str(e)}")
