from flask import Blueprint, request, jsonify
from backend.services.ga_service import run_ga

ga_blueprint = Blueprint("ga", __name__, url_prefix="/api/ga")

@ga_blueprint.route("/run", methods=["POST"])
def run():
    config = request.get_json()
    result = run_ga(config)
    return jsonify(result)
