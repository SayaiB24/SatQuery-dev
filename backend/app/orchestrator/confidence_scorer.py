from typing import List, Optional
from backend.app.schemas.api_models import Confidence, ConfidenceDetails
from backend.app.schemas.image_metadata import ImageMetadata
from backend.app.schemas.task_spec import TaskSpec


class ConfidenceScorer:
    """Computes auditable confidence tier and detailed rationale."""

    def compute(
        self,
        task_spec: TaskSpec,
        images: List[ImageMetadata],
        geometry_ok: bool,
        agreement_ok: bool,
        quantity_discrepancy: bool,
        verifier_rationale: str,
    ) -> Confidence:
        details = ConfidenceDetails(
            geometry_check=geometry_ok,
            cross_tool_agreement=agreement_ok,
            quantity_discrepancy=quantity_discrepancy,
        )

        # Severe errors -> Low
        if not geometry_ok or quantity_discrepancy:
            tier = "Low"
            rationale = verifier_rationale
            return Confidence(tier=tier, rationale=rationale, details=details)

        # High cloud obscuration -> Medium or Low
        avg_cloud = sum(img.cloud_mask_percent or 0.0 for img in images) / max(len(images), 1)
        if avg_cloud > 40.0 and task_spec.required_modalities == ["optical"]:
            tier = "Low"
            rationale = f"Optical imagery degraded by {avg_cloud:.1f}% cloud obscuration without radar penetration."
            return Confidence(tier=tier, rationale=rationale, details=details)

        # High confidence condition
        if geometry_ok and agreement_ok and not quantity_discrepancy and task_spec.intent_confidence >= 0.85:
            tier = "High"
            rationale = "High confidence: Multi-stage geometric bounds, specialist output agreement, and physical sensor parameters fully validated."
        else:
            tier = "Medium"
            rationale = "Moderate confidence: Analysis verified on available imagery with standard confidence thresholds."

        return Confidence(tier=tier, rationale=rationale, details=details)
