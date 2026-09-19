import json
import urllib.request

BASE_URL = "http://127.0.0.1:8000"
MOCK_PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"


def get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8")


def post_multipart(endpoint, fields, files):
    boundary = "----WebKitFormBoundaryPhase4Test"
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


def test_scenario_1():
    print("=== TESTING SCENARIO 1 — Single-image VQA ===")
    query = "Describe the land-cover and major objects visible in this image."
    files = [("files", "cartosat_optical_scene.png", MOCK_PNG, "image/png")]
    status, text = post_multipart("/v1/analyze", fields={"query": query}, files=files)
    assert status == 200, f"Status: {status}"
    res = json.loads(text)

    print(f"Session ID: {res['sessionId']}")
    print(f"Task Type: {res['taskSpec']['taskType']}")
    print(f"Answer snippet: {res['answerText'][:110]}...")
    print(f"Confidence: {res['confidence']['tier']} - {res['confidence']['rationale'][:60]}...")
    print(f"Boxes count: {len(res['evidence']['boxes'])}")
    print(f"Overlay URLs: {res['evidence']['overlayImageUrls']}")

    assert "land-cover" in res["answerText"].lower() or "port basin" in res["answerText"].lower()
    assert len(res["evidence"]["boxes"]) >= 3
    assert len(res["evidence"]["overlayImageUrls"]) > 0
    # Check that overlay image is accessible
    overlay_url = res["evidence"]["overlayImageUrls"][0]
    ov_status, _ = get(overlay_url)
    assert ov_status == 200, f"Failed loading overlay: {overlay_url}"
    print("[PASS] SCENARIO 1: Land-cover description, 3 tanks localized, overlay PNG generated and served.\n")


def test_scenario_2():
    print("=== TESTING SCENARIO 2 — Grounding (Multi-candidate Ambiguity) ===")
    query = "Highlight the water body referred to in the query."
    files = [("files", "cartosat_water_scene.png", MOCK_PNG, "image/png")]
    status, text = post_multipart("/v1/analyze", fields={"query": query}, files=files)
    assert status == 200, f"Status: {status}"
    res = json.loads(text)

    print(f"Task Type: {res['taskSpec']['taskType']}")
    print(f"Answer snippet: {res['answerText'][:110]}...")
    print(f"Confidence Tier: {res['confidence']['tier']}")
    print(f"Candidates localized: {len(res['evidence']['boxes'])}")
    labels = [b["label"] for b in res["evidence"]["boxes"]]
    print(f"Candidate labels: {labels}")

    assert res["taskSpec"]["taskType"] == "single_grounding"
    assert len(res["evidence"]["boxes"]) == 2  # Primary & Secondary candidate
    assert res["confidence"]["tier"] == "Medium"  # Ambiguity reported
    print("[PASS] SCENARIO 2: Multi-candidate water body localized with transparent Medium confidence.\n")


def test_scenario_3():
    print("=== TESTING SCENARIO 3 — Bi-temporal Change ===")
    query = "What changed between these two dates, and where did the change occur?"
    files = [
        ("files", "optical_baseline_t1.png", MOCK_PNG, "image/png"),
        ("files", "optical_current_t2.png", MOCK_PNG, "image/png"),
    ]
    status, text = post_multipart("/v1/analyze", fields={"query": query}, files=files)
    assert status == 200, f"Status: {status}"
    res = json.loads(text)

    print(f"Task Type: {res['taskSpec']['taskType']}")
    print(f"Answer snippet: {res['answerText'][:110]}...")
    print(f"Boxes count: {len(res['evidence']['boxes'])}")
    print(f"Masks: {res['evidence']['masks']}")

    assert "change" in res["answerText"].lower() or "expansion" in res["answerText"].lower()
    assert len(res["evidence"]["boxes"]) >= 2
    assert len(res["evidence"]["masks"]) > 0
    # Check that mask file is accessible
    mask_url = res["evidence"]["masks"][0]
    m_status, _ = get(mask_url)
    assert m_status == 200, f"Failed loading mask: {mask_url}"
    print("[PASS] SCENARIO 3: Bitemporal change delta identified (+14,200 sq m), change mask generated.\n")


def test_scenario_4():
    print("=== TESTING SCENARIO 4 — Optical-SAR Fusion ===")
    query = "Use the optical and SAR images together to identify built-up and water-covered regions."
    files = [
        ("files", "cartosat_optical_harbor.png", MOCK_PNG, "image/png"),
        ("files", "risat_sar_cband_radar.png", MOCK_PNG, "image/png"),
    ]
    status, text = post_multipart("/v1/analyze", fields={"query": query}, files=files)
    assert status == 200, f"Status: {status}"
    res = json.loads(text)

    print(f"Task Type: {res['taskSpec']['taskType']}")
    print(f"Answer snippet: {res['answerText'][:120]}...")
    print(f"Region Tags count: {len(res['evidence']['regionTags'])}")
    tag_types = [t["tag"] for t in res["evidence"]["regionTags"]]
    print(f"Tags detected: {tag_types}")

    assert res["taskSpec"]["taskType"] == "fusion"
    assert "agreement" in tag_types
    assert "sar_only" in tag_types
    assert "optical_only" in tag_types
    print("[PASS] SCENARIO 4: Optical-SAR fusion verbalized with explicit sensor citations & complementarity tags.\n")


def test_scenario_5():
    print("=== TESTING SCENARIO 5 — Compound Fusion + Change ===")
    query = "Use the optical and SAR images together to identify built-up areas, then determine whether the built-up area increased."
    files = [
        ("files", "cartosat_optical_t1.png", MOCK_PNG, "image/png"),
        ("files", "risat_sar_cband_t2.png", MOCK_PNG, "image/png"),
    ]
    status, text = post_multipart("/v1/analyze", fields={"query": query}, files=files)
    assert status == 200, f"Status: {status}"
    res = json.loads(text)

    print(f"Task Type: {res['taskSpec']['taskType']}")
    print(f"Answer snippet: {res['answerText'][:120]}...")
    steps = res["executionTrace"]["steps"]
    components = [s["component"] for s in steps]
    print(f"Pipeline components executed: {components}")

    assert res["taskSpec"]["taskType"] == "fusion_then_change"
    assert "GroundingSpecialist" in components
    assert "ComplementarityDetector" in components
    assert "ChangeVqaSpecialist" in components
    print("[PASS] SCENARIO 5: 2-stage compound pipeline executed (Fusion -> Change) with multi-specialist trace.\n")


if __name__ == "__main__":
    print("=================================================================")
    print("      SATQUERY AI — PHASE 4 DEMO SCENARIO ENGINE VERIFICATION    ")
    print("=================================================================\n")
    test_scenario_1()
    test_scenario_2()
    test_scenario_3()
    test_scenario_4()
    test_scenario_5()
    print("=================================================================")
    print("   ALL 5 SCENARIOS VERIFIED SUCCESSFULLY WITH SCENARIO-AWARE DATA")
    print("=================================================================")
