from flask import Blueprint, request, jsonify, send_from_directory
from backend.services.ga_service import run_ga
from backend.services.io_service import persist_result

ga_blueprint = Blueprint("ga", __name__)

@ga_blueprint.route("/run", methods=["POST"])
def run():
    config = request.get_json()
    result = run_ga(config)
    persist_result(result)

    return jsonify(result)

@ga_blueprint.route("/", methods=["GET"])
def index():
    """
    Serve the index page.
    :return: Rendered HTML page.
    """
    return send_from_directory('frontend', 'stronka.html')

@ga_blueprint.route("/style.css", methods=["GET"])
def send_csv():
    """
    Serve a file from the static folder.
    :return: The file.
    """
    return send_from_directory('frontend', 'style.css')
