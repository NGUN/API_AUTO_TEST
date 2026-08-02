from config import username, password
from utils.yaml_utils import load_yaml

yaml_data = load_yaml("data/login_data.yaml")

login_cases = yaml_data["login_cases"]

for case in login_cases:
	if case["username"] == "${API_USERNAME}":
		case["username"] = username

	if case["password"] == "${API_PASSWORD}":
		case["password"] = password

login_case_ids = [
	case["id"] for case in login_cases
]