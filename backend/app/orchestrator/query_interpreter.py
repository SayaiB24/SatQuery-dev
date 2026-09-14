import re
from typing import List, Optional
from backend.app.schemas.image_metadata import ImageMetadata
from backend.app.schemas.task_spec import TaskSpec, TaskType


class QueryInterpreter:
    """Classifies natural language query into a formal TaskSpec."""

    def interpret(self, query: str, images: List[ImageMetadata]) -> TaskSpec:
        q = query.strip()
        q_lower = q.lower()
        image_count = len(images)

        # Check for ambiguity
        if len(q) < 4 or q_lower in ["hello", "hi", "test", "what", "where"]:
            return TaskSpec(
                task_type=TaskType.SINGLE_VQA,
                status="ambiguous",
                target_object=None,
                question_text=q,
                required_image_count=1,
                required_modalities=["optical"],
                requires_temporal_pairing=False,
                intent_confidence=0.35,
                clarifying_question="Query is underspecified. Please specify targets (e.g., 'Locate all fuel storage tanks' or 'Identify maritime vessels').",
            )

        # Modalities present in input
        modalities = [img.detected_modality for img in images]
        has_sar = "sar" in modalities
        has_optical = any(m in ["optical", "multispectral"] for m in modalities)

        # 1. Change detection intents
        change_keywords = ["change", "difference", "between", "expansion", "growth", "demolition", "new construction", "2023", "2024", "before and after"]
        is_change_query = any(k in q_lower for k in change_keywords)

        if is_change_query or image_count >= 2:
            if has_sar and has_optical and not is_change_query:
                # Multi-modal fusion
                return TaskSpec(
                    task_type=TaskType.FUSION,
                    status="resolved",
                    target_object=self._extract_target(q_lower),
                    question_text=q,
                    required_image_count=2,
                    required_modalities=["optical", "sar"],
                    requires_temporal_pairing=False,
                    intent_confidence=0.96,
                )
            elif is_change_query:
                if any(w in q_lower for w in ["locate", "box", "detect", "ground"]):
                    task_type = TaskType.CHANGE_AND_GROUNDING
                elif any(w in q_lower for w in ["describe", "summary", "overview"]):
                    task_type = TaskType.CHANGE_DESCRIPTION
                else:
                    task_type = TaskType.CHANGE_VQA

                return TaskSpec(
                    task_type=task_type,
                    status="resolved",
                    target_object=self._extract_target(q_lower),
                    question_text=q,
                    required_image_count=2,
                    required_modalities=["optical", "optical"],
                    requires_temporal_pairing=True,
                    intent_confidence=0.94,
                )

        # 2. Grounding / Localization intents
        grounding_keywords = ["locate", "detect", "ground", "find", "bounding box", "coordinates", "where are", "show me all"]
        if any(k in q_lower for k in grounding_keywords):
            return TaskSpec(
                task_type=TaskType.SINGLE_GROUNDING,
                status="resolved",
                target_object=self._extract_target(q_lower),
                question_text=q,
                required_image_count=1,
                required_modalities=["optical"],
                requires_temporal_pairing=False,
                intent_confidence=0.95,
            )

        # 3. Captioning intents
        if any(k in q_lower for k in ["describe", "caption", "scene summary", "overview"]):
            return TaskSpec(
                task_type=TaskType.SINGLE_CAPTION,
                status="resolved",
                target_object=None,
                question_text=q,
                required_image_count=1,
                required_modalities=["optical"],
                requires_temporal_pairing=False,
                intent_confidence=0.92,
            )

        # 4. Default to Single-Image VQA
        return TaskSpec(
            task_type=TaskType.SINGLE_VQA,
            status="resolved",
            target_object=self._extract_target(q_lower),
            question_text=q,
            required_image_count=1,
            required_modalities=["optical"],
            requires_temporal_pairing=False,
            intent_confidence=0.90,
        )

    def _extract_target(self, q_lower: str) -> Optional[str]:
        if "tank" in q_lower:
            return "fuel storage tanks"
        if "vessel" in q_lower or "ship" in q_lower or "boat" in q_lower:
            return "maritime vessels"
        if "aircraft" in q_lower or "plane" in q_lower or "runway" in q_lower:
            return "aircraft / runway"
        if "building" in q_lower or "structure" in q_lower:
            return "buildings / infrastructure"
        return "infrastructure features"
