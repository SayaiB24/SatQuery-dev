import asyncio
import json
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://127.0.0.1:8000"
MOCK_PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"


def get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8")


def post_multipart(endpoint, fields, files):
    boundary = "----WebKitFormBoundaryPhase3Test"
    body = bytearray()

    for k, v in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{v}\r\n".encode("utf-8"))

    for k, filename, content, content_type in files:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{k}"; filename="{filename}"\r\n'.encode("utf-8"))
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8")


def run_phase3_tests():
    print("=================================================================")
    print("          SATQUERY AI — PHASE 3 ORCHESTRATION PIPELINE TESTS      ")
    print("=================================================================\n")

    # 1. Test System Health & Registry
    status, text = get("/v1/health")
    assert status == 200, f"Health check failed: {status}"
    health_data = json.loads(text)
    print(f"[PASS] [HEALTH] {health_data['service']} v{health_data['version']} is online.")

    status, text = get("/v1/registry")
    assert status == 200, f"Registry check failed: {status}"
    reg_data = json.loads(text)
    print(f"[PASS] [REGISTRY] {len(reg_data['specialists'])} specialists, {len(reg_data['preconditions'])} precondition rules registered.\n")

    # 2. Test All 8 Task Types via Orchestrator Pipeline
    task_tests = [
        {
            "name": "Task 1: single_vqa",
            "query": "How many fuel storage tanks are visible in the terminal?",
            "files": [("files", "optical_terminal.png", MOCK_PNG, "image/png")],
            "expected_task_type": "single_vqa",
            "check": lambda res: res["rejected"] is False and len(res["evidence"]["boxes"]) > 0,
        },
        {
            "name": "Task 2: single_caption",
            "query": "Describe the scene and major installations visible in this image",
            "files": [("files", "optical_scene.png", MOCK_PNG, "image/png")],
            "expected_task_type": "single_caption",
            "check": lambda res: res["rejected"] is False and "port" in res["answerText"].lower(),
        },
        {
            "name": "Task 3: single_grounding",
            "query": "Locate and highlight all fuel storage tanks in the facility",
            "files": [("files", "optical_tanks.png", MOCK_PNG, "image/png")],
            "expected_task_type": "single_grounding",
            "check": lambda res: res["rejected"] is False and len(res["evidence"]["boxes"]) == 3,
        },
        {
            "name": "Task 4: change_vqa",
            "query": "What infrastructure changes occurred between 2023 and 2024?",
            "files": [
                ("files", "optical_2023.png", MOCK_PNG, "image/png"),
                ("files", "optical_2024.png", MOCK_PNG, "image/png"),
            ],
            "expected_task_type": "change_vqa",
            "check": lambda res: res["rejected"] is False and "expansion" in res["answerText"].lower(),
        },
        {
            "name": "Task 5: change_description",
            "query": "Describe the land-use changes that occurred between baseline and current acquisitions",
            "files": [
                ("files", "optical_t1.png", MOCK_PNG, "image/png"),
                ("files", "optical_t2.png", MOCK_PNG, "image/png"),
            ],
            "expected_task_type": "change_description",
            "check": lambda res: res["rejected"] is False and "staging area" in res["answerText"].lower(),
        },
        {
            "name": "Task 6: change_and_grounding",
            "query": "Locate and highlight all new infrastructure built between 2023 and 2024",
            "files": [
                ("files", "optical_t1.png", MOCK_PNG, "image/png"),
                ("files", "optical_t2.png", MOCK_PNG, "image/png"),
            ],
            "expected_task_type": "change_and_grounding",
            "check": lambda res: res["rejected"] is False and len(res["evidence"]["boxes"]) > 0,
        },
        {
            "name": "Task 7: fusion",
            "query": "Detect all naval vessels in the harbor under cloud cover using optical and SAR",
            "files": [
                ("files", "cartosat_optical.png", MOCK_PNG, "image/png"),
                ("files", "risat_sar_cband.png", MOCK_PNG, "image/png"),
            ],
            "expected_task_type": "fusion",
            "check": lambda res: res["rejected"] is False and res["evidence"]["regionTags"] is not None and len(res["evidence"]["regionTags"]) == 3,
        },
        {
            "name": "Task 8: fusion_then_change (Compound)",
            "query": "Use optical and SAR to identify built-up areas, then determine whether built-up area increased",
            "files": [
                ("files", "cartosat_optical.png", MOCK_PNG, "image/png"),
                ("files", "risat_sar_cband.png", MOCK_PNG, "image/png"),
            ],
            "expected_task_type": "fusion_then_change",
            "check": lambda res: res["rejected"] is False and "fused" in res["answerText"].lower() and "temporal" in res["answerText"].lower(),
        },
    ]

    print("--- TESTING ALL 8 TASK TYPES ---")
    created_sessions = []
    for test in task_tests:
        status, text = post_multipart("/v1/analyze", fields={"query": test["query"]}, files=test["files"])
        assert status == 200, f"Failed {test['name']} with status {status}"
        res = json.loads(text)
        created_sessions.append(res["sessionId"])

        actual_task_type = res["taskSpec"]["taskType"]
        assert actual_task_type == test["expected_task_type"], (
            f"Task type mismatch for {test['name']}: expected {test['expected_task_type']}, got {actual_task_type}"
        )
        assert test["check"](res), f"Custom check failed for {test['name']}"

        # Check execution trace steps exist
        steps = res["executionTrace"]["steps"]
        assert len(steps) >= 5, f"Execution trace steps insufficient for {test['name']}: {len(steps)}"

        print(f"[PASS] [{test['name']}] -> Resolved as '{actual_task_type}', {len(steps)} trace steps, Confidence: {res['confidence']['tier']}")

    print("\n--- TESTING VALIDATION PRECONDITION REJECTIONS ---")
    # 3. Test Validation Rejection Preconditions
    rejection_tests = [
        {
            "name": "Rejection 1: ambiguous_intent",
            "query": "what",
            "files": [("files", "optical.png", MOCK_PNG, "image/png")],
            "expected_code": "ambiguous_intent",
        },
        {
            "name": "Rejection 2: insufficient_image_count",
            "query": "What infrastructure changes occurred between 2023 and 2024?",
            "files": [("files", "optical_single.png", MOCK_PNG, "image/png")],
            "expected_code": "insufficient_image_count",
        },
        {
            "name": "Rejection 3: modality_mismatch",
            "query": "What infrastructure changes occurred between 2023 and 2024?",
            "files": [
                ("files", "optical_base.png", MOCK_PNG, "image/png"),
                ("files", "sar_radar.png", MOCK_PNG, "image/png"),
            ],
            "expected_code": "modality_mismatch",
        },
        {
            "name": "Rejection 4: unsupported_format",
            "query": "Locate fuel tanks",
            "files": [("files", "image.bmp", MOCK_PNG, "image/bmp")],
            "expected_code": "unsupported_format",
        },
    ]

    for rtest in rejection_tests:
        status, text = post_multipart("/v1/analyze", fields={"query": rtest["query"]}, files=rtest["files"])
        assert status == 200, f"Rejection endpoint call failed: {status}"
        res = json.loads(text)
        assert res["rejected"] is True, f"Expected rejected=True for {rtest['name']}"
        actual_code = res["rejectionDetails"]["reasonCode"]
        assert actual_code == rtest["expected_code"], (
            f"Expected code {rtest['expected_code']}, got {actual_code} for {rtest['name']}"
        )
        assert res["rejectionReason"] is not None
        assert res["executionTrace"]["rejection"] is not None
        print(f"[PASS] [{rtest['name']}] -> Rejected with code '{actual_code}': {res['rejectionReason'][:60]}...")

    print("\n--- TESTING SESSION PERSISTENCE & REPORT EXPORT ---")
    test_session = created_sessions[0]
    status, text = get(f"/v1/session/{test_session}")
    assert status == 200, f"Failed GET session: {status}"
    sess_obj = json.loads(text)
    assert sess_obj["sessionId"] == test_session
    print(f"[PASS] [SESSION RETRIEVAL] Session {test_session} retrieved successfully.")

    status, text = get(f"/v1/session/{test_session}/report?format=json")
    assert status == 200, f"Failed JSON report export: {status}"
    rep_obj = json.loads(text)
    assert rep_obj["sessionId"] == test_session
    print(f"[PASS] [REPORT JSON] Full JSON report downloaded.")

    status, text = get(f"/v1/session/{test_session}/report?format=pdf")
    assert status == 200, f"Failed PDF report export: {status}"
    assert "<!DOCTYPE html>" in text
    print(f"[PASS] [REPORT PDF/HTML] Printable report generated with data parity.")

    print("\n=================================================================")
    print("   ALL PHASE 3 ORCHESTRATION PIPELINE TESTS PASSED (100% SUCCESS) ")
    print("=================================================================")


if __name__ == "__main__":
    run_phase3_tests()
