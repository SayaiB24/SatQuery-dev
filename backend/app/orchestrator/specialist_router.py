from typing import List, Tuple
from backend.app.fusion_pipeline.complementarity_detector import ComplementarityDetector
from backend.app.fusion_pipeline.verbalizer import MultimodalVerbalizer
from backend.app.schemas.evidence import BoundingBox, EvidenceItem, RegionTag
from backend.app.schemas.image_metadata import ImageMetadata
from backend.app.schemas.task_spec import TaskSpec, TaskType
from backend.app.specialists.change_vqa import ChangeVqaSpecialist
from backend.app.specialists.grounding import GroundingSpecialist
from backend.app.specialists.vqa_caption import VqaCaptionSpecialist


class SpecialistRouter:
    """Routes validated TaskSpecs to specialist models and fusion pipelines."""

    def __init__(self):
        self.vqa_specialist = VqaCaptionSpecialist()
        self.grounding_specialist = GroundingSpecialist()
        self.change_specialist = ChangeVqaSpecialist()
        self.complementarity_detector = ComplementarityDetector()
        self.verbalizer = MultimodalVerbalizer()

    async def route_and_execute(
        self,
        task_spec: TaskSpec,
        images: List[ImageMetadata],
        session_id: str,
    ) -> Tuple[List[EvidenceItem], str, List[BoundingBox], List[RegionTag]]:
        items: List[EvidenceItem] = []
        boxes: List[BoundingBox] = []
        region_tags: List[RegionTag] = []
        answer_text = ""

        tt = task_spec.task_type

        if tt == TaskType.FUSION or tt == TaskType.FUSION_THEN_CHANGE:
            # 1. Multi-modal fusion
            g_item = await self.grounding_specialist.execute(images, task_spec, session_id)
            items.append(g_item)
            boxes = g_item.boxes

            region_tags = self.complementarity_detector.detect_tags(
                optical_boxes=boxes,
                sar_boxes=boxes,
                query=task_spec.question_text or "",
            )

            answer_text = self.verbalizer.verbalize(
                query=task_spec.question_text or "",
                boxes=boxes,
                region_tags=region_tags,
            )

            v_item = EvidenceItem(
                source_specialist="Multimodal Optical-SAR Fusion Pipeline",
                adapter_id="fusion_verbalizer_v1.0",
                answer_text=answer_text,
                boxes=boxes,
                region_tags=region_tags,
                deterministic_pixel_count=len(boxes),
                quantity_flag=True,
                geometry_valid=True,
                quantity_discrepancy=False,
            )
            items.append(v_item)

        elif tt in [TaskType.CHANGE_VQA, TaskType.CHANGE_DESCRIPTION, TaskType.CHANGE_AND_GROUNDING]:
            # 2. Change detection
            c_item = await self.change_specialist.execute(images, task_spec, session_id)
            items.append(c_item)
            boxes = c_item.boxes
            answer_text = c_item.answer_text or ""

            if tt == TaskType.CHANGE_AND_GROUNDING:
                g_item = await self.grounding_specialist.execute(images, task_spec, session_id)
                items.append(g_item)

        elif tt == TaskType.SINGLE_GROUNDING:
            # 3. Grounding
            g_item = await self.grounding_specialist.execute(images, task_spec, session_id)
            items.append(g_item)
            boxes = g_item.boxes
            answer_text = g_item.answer_text or ""

        elif tt in [TaskType.SINGLE_VQA, TaskType.SINGLE_CAPTION]:
            # 4. VQA / Caption
            v_item = await self.vqa_specialist.execute(images, task_spec, session_id)
            items.append(v_item)
            answer_text = v_item.answer_text or ""

            # If counting or objects implied, run grounding specialist too
            if v_item.quantity_flag:
                g_item = await self.grounding_specialist.execute(images, task_spec, session_id)
                items.append(g_item)
                boxes = g_item.boxes

        return items, answer_text, boxes, region_tags
