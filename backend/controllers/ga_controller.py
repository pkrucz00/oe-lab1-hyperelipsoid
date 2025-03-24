from flask import Blueprint, request, jsonify
from backend.services.ga_service import run_ga
from backend.services.io_service import persist_result

ga_blueprint = Blueprint("ga", __name__, url_prefix="/api/ga")

@ga_blueprint.route("/run", methods=["POST"])
def run():
    config = request.get_json()
    result = run_ga(config)
    persist_result(result)

    return jsonify(result)
