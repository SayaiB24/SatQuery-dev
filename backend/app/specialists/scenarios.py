from typing import Any, Dict, List, Optional
from backend.app.schemas.evidence import BoundingBox, EvidenceItem, RegionTag
from backend.app.schemas.task_spec import TaskSpec


def get_scenario_grounding_boxes(query: str) -> List[BoundingBox]:
    """Returns realistic bounding boxes based on query contents."""
    q = query.lower()
    if "tank" in q:
        return [
            BoundingBox(
                id="box_tank_01",
                label="Fuel Storage Tank (Floating Roof)",
                x_left=18.4,
                y_top=24.1,
                x_right=34.8,
                y_bottom=41.5,
                score=0.96,
                is_primary=True,
            ),
            BoundingBox(
                id="box_tank_02",
                label="Fuel Storage Tank (Fixed Roof)",
                x_left=42.1,
                y_top=28.5,
                x_right=58.2,
                y_bottom=45.9,
                score=0.94,
                is_primary=True,
            ),
            BoundingBox(
                id="box_tank_03",
                label="Industrial Tank (Cooling / Secondary)",
                x_left=65.0,
                y_top=52.0,
                x_right=81.2,
                y_bottom=69.4,
                score=0.88,
                is_primary=True,
            ),
        ]
    elif "vessel" in q or "ship" in q or "boat" in q or "harbor" in q:
        return [
            BoundingBox(
                id="box_vessel_01",
                label="Cargo Vessel (Container Berth 4)",
                x_left=22.5,
                y_top=14.2,
                x_right=44.1,
                y_bottom=32.8,
                score=0.97,
                is_primary=True,
            ),
            BoundingBox(
                id="box_vessel_02",
                label="Bulk Carrier Vessel (Berth 7)",
                x_left=51.0,
                y_top=38.4,
                x_right=73.6,
                y_bottom=57.2,
                score=0.93,
                is_primary=True,
            ),
            BoundingBox(
                id="box_vessel_03",
                label="Patrol / Service Tugboat",
                x_left=12.2,
                y_top=64.8,
                x_right=26.4,
                y_bottom=78.5,
                score=0.89,
                is_primary=False,
            ),
        ]
    elif "change" in q or "construction" in q or "expansion" in q:
        return [
            BoundingBox(
                id="box_change_01",
                label="New Pier & Crane Foundation Expansion",
                x_left=35.0,
                y_top=22.0,
                x_right=62.0,
                y_bottom=54.0,
                score=0.95,
                is_primary=True,
            ),
            BoundingBox(
                id="box_change_02",
                label="Cleared Staging Logistics Lot (+14,200 sq m)",
                x_left=68.0,
                y_top=45.0,
                x_right=88.5,
                y_bottom=72.0,
                score=0.91,
                is_primary=True,
            ),
        ]
    elif "runway" in q or "airport" in q or "aircraft" in q:
        return [
            BoundingBox(
                id="box_plane_01",
                label="Commercial Narrowbody Aircraft (Gate A3)",
                x_left=28.0,
                y_top=35.0,
                x_right=46.0,
                y_bottom=52.0,
                score=0.94,
                is_primary=True,
            ),
            BoundingBox(
                id="box_plane_02",
                label="Commercial Widebody Aircraft (Gate B1)",
                x_left=54.0,
                y_top=48.0,
                x_right=76.0,
                y_bottom=68.0,
                score=0.92,
                is_primary=True,
            ),
        ]
    else:
        # Default high-fidelity remote sensing bounding boxes
        return [
            BoundingBox(
                id="box_feat_01",
                label="Primary Detected Structure / Feature",
                x_left=25.0,
                y_top=25.0,
                x_right=55.0,
                y_bottom=55.0,
                score=0.91,
                is_primary=True,
            ),
            BoundingBox(
                id="box_feat_02",
                label="Secondary Auxiliary Infrastructure",
                x_left=60.0,
                y_top=40.0,
                x_right=82.0,
                y_bottom=70.0,
                score=0.86,
                is_primary=True,
            ),
        ]


def get_scenario_fusion_tags(query: str) -> List[RegionTag]:
    """Returns multi-sensor complementarity tags for fusion pipelines."""
    return [
        RegionTag(
            region="North Pier / Mooring Slip",
            tag="agreement",
            score=0.96,
            description="Optical RGB and SAR double-bounce radar return both clearly confirm 2 large maritime vessels moored at berths 4 and 7.",
        ),
        RegionTag(
            region="Cloud-Occluded East Channel",
            tag="sar_only",
            score=0.91,
            description="Dense 42% cumulus cloud cover in Optical RGB is fully penetrated by SAR C-band microwave backscatter, discovering 1 additional cargo vessel.",
        ),
        RegionTag(
            region="Inland Container Staging Yard",
            tag="optical_only",
            score=0.88,
            description="Color-coded TEU shipping containers and painted taxiway lane markers resolved only via Optical high-resolution multispectral bands.",
        ),
    ]
