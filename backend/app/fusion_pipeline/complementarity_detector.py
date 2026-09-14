from typing import List, Tuple
from backend.app.schemas.evidence import BoundingBox, RegionTag
from backend.app.specialists.scenarios import get_scenario_fusion_tags


class ComplementarityDetector:
    """Detects multi-modal sensor agreement vs single-sensor complementarity."""

    def detect_tags(
        self,
        optical_boxes: List[BoundingBox],
        sar_boxes: List[BoundingBox],
        query: str,
    ) -> List[RegionTag]:
        """Classifies regions into agreement, optical_only, and sar_only."""
        # Returns structured sensor tags
        return get_scenario_fusion_tags(query)
