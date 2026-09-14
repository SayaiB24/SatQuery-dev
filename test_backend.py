import io
import json
import urllib.request
import urllib.error
import urllib.parse

BASE_URL = "http://127.0.0.1:8000"

def get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8")

def post_multipart(endpoint, fields, files):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
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
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8")

def run_tests():
    print("=== TEST 1: GET /v1/health ===")
    status, text = get("/v1/health")
    print(f"Status: {status}")
    health = json.loads(text)
    print(f"Health output: {json.dumps(health, indent=2)}")
    assert health["status"] == "ok"
    print("PASS TEST 1\n")

    print("=== TEST 2: GET /v1/registry ===")
    status, text = get("/v1/registry")
    print(f"Status: {status}")
    reg = json.loads(text)
    print(f"Specialists registered: {len(reg['specialists'])}")
    print(f"Preconditions registered: {len(reg['preconditions'])}")
    assert len(reg["specialists"]) >= 4
    assert len(reg["preconditions"]) >= 7
    print("PASS TEST 2\n")

    print("=== TEST 3: POST /v1/analyze (Single Optical VQA / Counting) ===")
    mock_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    status, text = post_multipart(
        "/v1/analyze",
        fields={"query": "How many fuel storage tanks are visible in the terminal?"},
        files=[("files", "optical_tank_terminal.png", mock_png, "image/png")]
    )
    print(f"Status: {status}")
    res1 = json.loads(text)
    session_id_1 = res1["sessionId"]
    print(f"Session ID: {session_id_1}")
    print(f"Task Type: {res1['taskSpec']['taskType']}")
    print(f"Answer: {res1['answerText']}")
    print(f"Confidence: {res1['confidence']['tier']} - {res1['confidence']['rationale']}")
    print(f"Evidence boxes count: {len(res1['evidence']['boxes'])}")
    print(f"Execution trace steps: {len(res1['executionTrace']['steps'])}")
    assert res1["rejected"] is False
    assert len(res1["evidence"]["boxes"]) > 0
    print("PASS TEST 3\n")

    print("=== TEST 4: POST /v1/analyze (Optical + SAR Multi-modal Fusion) ===")
    status, text = post_multipart(
        "/v1/analyze",
        fields={"query": "Detect all naval vessels in the harbor under cloud cover"},
        files=[
            ("files", "cartosat_optical_harbor.png", mock_png, "image/png"),
            ("files", "risat_sar_cband_harbor.png", mock_png, "image/png")
        ]
    )
    print(f"Status: {status}")
    res2 = json.loads(text)
    session_id_2 = res2["sessionId"]
    print(f"Session ID: {session_id_2}")
    print(f"Task Type: {res2['taskSpec']['taskType']}")
    print(f"Answer: {res2['answerText']}")
    print(f"Region tags: {len(res2['evidence']['regionTags'])}")
    assert res2["taskSpec"]["taskType"] == "fusion"
    assert res2["evidence"]["regionTags"] is not None
    print("PASS TEST 4\n")

    print("=== TEST 5: POST /v1/analyze (Validation Rejection Demo) ===")
    status, text = post_multipart(
        "/v1/analyze",
        fields={"query": "What infrastructure changes occurred between 2023 and 2024?"},
        files=[
            ("files", "optical_baseline_2023.png", mock_png, "image/png"),
            ("files", "sar_radar_2024.png", mock_png, "image/png")
        ]
    )
    print(f"Status: {status}")
    res3 = json.loads(text)
    print(f"Rejected: {res3['rejected']}")
    print(f"Rejection Reason: {res3['rejectionReason']}")
    print(f"Reason Code: {res3['rejectionDetails']['reasonCode']}")
    assert res3["rejected"] is True
    assert res3["rejectionDetails"]["reasonCode"] == "modality_mismatch"
    print("PASS TEST 5\n")

    print(f"=== TEST 6: GET /v1/session/{session_id_1} ===")
    status, text = get(f"/v1/session/{session_id_1}")
    print(f"Status: {status}")
    sess = json.loads(text)
    assert sess["sessionId"] == session_id_1
    assert sess["answerText"] == res1["answerText"]
    print("PASS TEST 6\n")

    print(f"=== TEST 7: GET /v1/session/{session_id_1}/report?format=json ===")
    status, text = get(f"/v1/session/{session_id_1}/report?format=json")
    print(f"Status: {status}")
    rep_json = json.loads(text)
    assert rep_json["sessionId"] == session_id_1
    print("PASS TEST 7\n")

    print(f"=== TEST 8: GET /v1/session/{session_id_1}/report?format=pdf ===")
    status, text = get(f"/v1/session/{session_id_1}/report?format=pdf")
    print(f"Status: {status}")
    assert "<!DOCTYPE html>" in text
    assert session_id_1 in text
    print("PASS TEST 8\n")

    print("ALL TESTS PASSED SUCCESSFULLY! Phase 2 backend verification complete.")

if __name__ == "__main__":
    run_tests()
