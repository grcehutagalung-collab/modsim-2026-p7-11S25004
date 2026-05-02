from flask import Blueprint, request, jsonify
from app.services.story_service import create_story, get_all_stories, delete_story

story_bp = Blueprint("story_bp", __name__)


@story_bp.route("/stories/generate", methods=["POST"])
def generate():
    """
    POST /stories/generate
    Body JSON: { "theme": "...", "genre": "fiksi|horor|romantis", "length": "pendek|sedang|panjang" }
    """
    data = request.get_json()

    theme = data.get("theme", "").strip()
    genre = data.get("genre", "fiksi").strip()
    length = data.get("length", "pendek").strip()

    if not theme:
        return jsonify({"error": "Field 'theme' wajib diisi"}), 400

    valid_genres = ["fiksi", "horor", "romantis"]
    if genre not in valid_genres:
        return jsonify({"error": f"Genre harus salah satu dari: {', '.join(valid_genres)}"}), 400

    valid_lengths = ["pendek", "sedang", "panjang"]
    if length not in valid_lengths:
        return jsonify({"error": f"Panjang harus salah satu dari: {', '.join(valid_lengths)}"}), 400

    try:
        result = create_story(theme=theme, genre=genre, length=length)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@story_bp.route("/stories", methods=["GET"])
def list_stories():
    """
    GET /stories?page=1&per_page=10
    """
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        result = get_all_stories(page=page, per_page=per_page)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@story_bp.route("/stories/<int:story_id>", methods=["DELETE"])
def remove_story(story_id):
    """
    DELETE /stories/<id>
    """
    try:
        deleted = delete_story(story_id)
        if deleted is None:
            return jsonify({"error": f"Cerita dengan id {story_id} tidak ditemukan"}), 404
        return jsonify({"message": f"Cerita id {story_id} berhasil dihapus"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
