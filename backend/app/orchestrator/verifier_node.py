import re
from typing import List, Tuple
from backend.app.schemas.evidence import BoundingBox, EvidenceItem, EvidenceLedger
from backend.app.schemas.task_spec import TaskSpec


class VerifierNode:
    """Performs post-generation verification on specialist evidence."""

    def verify(
        self,
        task_spec: TaskSpec,
        items: List[EvidenceItem],
    ) -> Tuple[bool, bool, bool, str]:
        """Returns (geometry_ok, agreement_ok, quantity_discrepancy, rationale)."""
        geometry_ok = True
        agreement_ok = True
        quantity_discrepancy = False

        all_boxes: List[BoundingBox] = []
        vqa_text = ""

        for item in items:
            if item.answer_text:
                vqa_text += " " + item.answer_text
            all_boxes.extend(item.boxes)

            # Check individual item geometry validity
            if not item.geometry_valid:
                geometry_ok = False

        # Verify all coordinates bounded [0, 100]
        for b in all_boxes:
            if not (0.0 <= b.x_left <= 100.0 and 0.0 <= b.y_top <= 100.0 and
                    0.0 <= b.x_right <= 100.0 and 0.0 <= b.y_bottom <= 100.0):
                geometry_ok = False
                break
            if b.x_left >= b.x_right or b.y_top >= b.y_bottom:
                geometry_ok = False
                break

        # Quantitative cross-check
        # Extract numbers from VQA text if query was counting
        box_count = len(all_boxes)
        match = re.search(r'\b(\d+)\b', vqa_text)
        if match and box_count > 0:
            claimed_count = int(match.group(1))
            if claimed_count != box_count and claimed_count > 0:
                # E.g. VQA says 5 but only 3 boxes found
                quantity_discrepancy = True
                agreement_ok = False

        if not geometry_ok:
            rationale = "Geometric boundary check failed: Coordinates exceed normalized bounds [0, 100]."
        elif quantity_discrepancy:
            rationale = f"Quantity discrepancy flagged: Text claims {claimed_count} targets but {box_count} spatial features localized."
        else:
            rationale = "Verification passed: Spatial bounding boxes, geometry coordinates, and textual claims demonstrate full mutual consistency."

        return geometry_ok, agreement_ok, quantity_discrepancy, rationale
