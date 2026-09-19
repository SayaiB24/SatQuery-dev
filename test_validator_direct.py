from backend.app.orchestrator.compatibility_validator import CompatibilityValidator
from backend.app.schemas.image_metadata import ImageMetadata
from backend.app.schemas.task_spec import TaskSpec, TaskType
from backend.app.schemas.validation import RejectionReasonCode, ValidationPass, ValidationRejection


def test_validator_isolated():
    validator = CompatibilityValidator()

    # 1. Format Check: unsupported_format
    task = TaskSpec(task_type=TaskType.SINGLE_VQA, required_image_count=1)
    img_bad_fmt = ImageMetadata(image_id="1", name="test.gif", format="gif")
    res = validator.validate(task, [img_bad_fmt])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.UNSUPPORTED_FORMAT
    print("[PASS] Unit Test 1: unsupported_format")

    # 2. Count Check: insufficient_image_count
    task_change = TaskSpec(task_type=TaskType.CHANGE_VQA, required_image_count=2, requires_temporal_pairing=True)
    img_optical_1 = ImageMetadata(image_id="1", name="t1.png", format="png", detected_modality="optical")
    res = validator.validate(task_change, [img_optical_1])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.INSUFFICIENT_IMAGE_COUNT
    print("[PASS] Unit Test 2: insufficient_image_count")

    # 3. Modality Check: modality_mismatch (Optical + SAR for change)
    img_sar_2 = ImageMetadata(image_id="2", name="t2.png", format="png", detected_modality="sar")
    res = validator.validate(task_change, [img_optical_1, img_sar_2])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.MODALITY_MISMATCH
    print("[PASS] Unit Test 3: modality_mismatch")

    # 4. Temporal Check: temporal_ordering_invalid (T1 > T2)
    img_optical_t1_late = ImageMetadata(
        image_id="1", name="t1.png", format="png", detected_modality="optical",
        acquisition_timestamp="2024-05-01T00:00:00Z"
    )
    img_optical_t2_early = ImageMetadata(
        image_id="2", name="t2.png", format="png", detected_modality="optical",
        acquisition_timestamp="2023-01-01T00:00:00Z"
    )
    res = validator.validate(task_change, [img_optical_t1_late, img_optical_t2_early])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.TEMPORAL_ORDERING_INVALID
    print("[PASS] Unit Test 4: temporal_ordering_invalid")

    # 5. Spatial Overlap Check: insufficient_footprint_overlap (< 70%)
    img_optical_t1_ok = ImageMetadata(
        image_id="1", name="t1.png", format="png", detected_modality="optical",
        footprint_overlap_percent=45.0
    )
    img_optical_t2_ok = ImageMetadata(
        image_id="2", name="t2.png", format="png", detected_modality="optical"
    )
    res = validator.validate(task_change, [img_optical_t1_ok, img_optical_t2_ok])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.INSUFFICIENT_FOOTPRINT_OVERLAP
    print("[PASS] Unit Test 5: insufficient_footprint_overlap")

    # 6. CRS Check: crs_mismatch_unresolvable
    img_crs_1 = ImageMetadata(
        image_id="1", name="t1.png", format="png", detected_modality="optical",
        crs="EPSG:32643 (UTM Zone 43N)"
    )
    img_crs_2 = ImageMetadata(
        image_id="2", name="t2.png", format="png", detected_modality="optical",
        crs="UNRESOLVABLE_LOCAL_CAD_GRID"
    )
    res = validator.validate(task_change, [img_crs_1, img_crs_2])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.CRS_MISMATCH_UNRESOLVABLE
    print("[PASS] Unit Test 6: crs_mismatch_unresolvable")

    # 7. Ambiguous Intent: ambiguous_intent
    task_ambiguous = TaskSpec(task_type=TaskType.SINGLE_VQA, status="ambiguous")
    res = validator.validate(task_ambiguous, [img_optical_1])
    assert isinstance(res, ValidationRejection)
    assert res.reason_code == RejectionReasonCode.AMBIGUOUS_INTENT
    print("[PASS] Unit Test 7: ambiguous_intent")

    # 8. Clean Pass
    img_clean_1 = ImageMetadata(
        image_id="1", name="t1.png", format="png", detected_modality="optical",
        acquisition_timestamp="2023-01-01T00:00:00Z", footprint_overlap_percent=88.5
    )
    img_clean_2 = ImageMetadata(
        image_id="2", name="t2.png", format="png", detected_modality="optical",
        acquisition_timestamp="2024-05-01T00:00:00Z"
    )
    res = validator.validate(task_change, [img_clean_1, img_clean_2])
    assert isinstance(res, ValidationPass)
    print("[PASS] Unit Test 8: ValidationPass (all preconditions satisfied)")

    print("\nALL 8 COMPATIBILITY VALIDATOR TESTS PASSED!")


if __name__ == "__main__":
    test_validator_isolated()
