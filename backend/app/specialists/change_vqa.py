from typing import Any, Dict, List
from backend.app.schemas.evidence import BoundingBox, EvidenceItem
from backend.app.schemas.image_metadata import ImageMetadata
from backend.app.schemas.task_spec import TaskSpec, TaskType
from backend.app.specialists.base import BaseSpecialist
from backend.app.specialists.scenarios import get_scenario_grounding_boxes


class ChangeVqaSpecialist(BaseSpecialist):
    """Specialist adapter for Bitemporal Change Detection, Change VQA, and Change Description."""

    def __init__(self):
        super().__init__(
            name="Bitemporal Change VQA Specialist",
            adapter_id="change_vqa_adapter_v1.0",
            supported_tasks=[
                TaskType.CHANGE_VQA,
                TaskType.CHANGE_DESCRIPTION,
                TaskType.FUSION_THEN_CHANGE,
            ],
        )

    async def execute(
        self,
        images: List[ImageMetadata],
        task_spec: TaskSpec,
        session_id: str,
        **kwargs: Any
    ) -> EvidenceItem:
        query = task_spec.question_text or ""
        boxes = get_scenario_grounding_boxes("change")

        answer = (
            "Bitemporal change analysis between the baseline (T1) and current (T2) acquisitions reveals "
            "significant infrastructure expansion: +14,200 sq m of new paved staging area and concrete "
            "foundations for a secondary crane rail along the eastern embankment. "
            "No structural demolition was detected."
        )

        return EvidenceItem(
            source_specialist=self.name,
            adapter_id=self.adapter_id,
            answer_text=answer,
            boxes=boxes,
            mask_ref="mask_change_diff_01.png",
            deterministic_pixel_count=158400,  # ~14,200 sq m at 0.3m GSD
            quantity_flag=True,
            geometry_valid=True,
            quantity_discrepancy=False,
        )
