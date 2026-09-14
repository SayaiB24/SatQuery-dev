import uuid
from typing import Any, Dict, List, Optional
from backend.app.orchestrator.compatibility_validator import CompatibilityValidator
from backend.app.orchestrator.confidence_scorer import ConfidenceScorer
from backend.app.orchestrator.query_interpreter import QueryInterpreter
from backend.app.orchestrator.specialist_router import SpecialistRouter
from backend.app.orchestrator.trace_emitter import TraceEmitter
from backend.app.orchestrator.verifier_node import VerifierNode
from backend.app.schemas.api_models import AnalyzeResponse, Confidence, EvidenceVisuals
from backend.app.schemas.image_metadata import ImageMetadata
from backend.app.schemas.validation import ValidationPass, ValidationRejection
from backend.app.services.report_service import report_service
from backend.app.services.storage_service import storage_service


class OrchestratorService:
    """Master orchestrator executing the GeoGraphRAG & Verifier-in-the-Loop workflow."""

    def __init__(self):
        self.query_interpreter = QueryInterpreter()
        self.compatibility_validator = CompatibilityValidator()
        self.specialist_router = SpecialistRouter()
        self.verifier_node = VerifierNode()
        self.confidence_scorer = ConfidenceScorer()

    async def run_pipeline(
        self,
        query: str,
        images: List[ImageMetadata],
        session_id: Optional[str] = None,
        session_options: Optional[Dict[str, Any]] = None,
    ) -> AnalyzeResponse:
        session_id = session_id or f"sq-{uuid.uuid4().hex[:8]}"
        trace = TraceEmitter(session_id=session_id)

        # Step 1: Query Interpretation
        trace.add_step(
            component="QueryInterpreter",
            adapter_id="intent_classifier_v1.0",
            output_summary=f"Parsed natural language query: '{query}'",
            parameters={"query": query},
        )
        task_spec = self.query_interpreter.interpret(query, images)

        # Step 2: Compatibility Validation (Preconditions)
        trace.add_step(
            component="CompatibilityValidator",
            adapter_id="geographrag_preconditions_v1.0",
            output_summary=f"Evaluated physical preconditions for task '{task_spec.task_type.value}'",
            parameters={
                "required_image_count": task_spec.required_image_count,
                "input_images": [img.name for img in images],
            },
        )
        validation_result = self.compatibility_validator.validate(task_spec, images)

        # Handle Rejection gracefully
        if isinstance(validation_result, ValidationRejection):
            trace.add_step(
                component="PreconditionGate",
                adapter_id="rejection_handler_v1.0",
                output_summary=f"Analysis terminated: {validation_result.reason_code.value} - {validation_result.human_readable_reason}",
                status="rejected",
            )
            execution_trace = trace.build_trace(
                selected_task_type=task_spec.task_type.value,
                confidence_tier="Low",
                confidence_rationale="Execution halted by physical precondition validator.",
                rejection=validation_result,
            )

            response = AnalyzeResponse(
                session_id=session_id,
                answer_text=None,
                evidence=EvidenceVisuals(),
                confidence=Confidence(
                    tier="Low",
                    rationale="Execution halted: Input imagery does not satisfy satellite remote sensing preconditions.",
                ),
                execution_trace=execution_trace,
                report_url=f"/v1/session/{session_id}/report",
                rejected=True,
                rejection_reason=validation_result.human_readable_reason,
                rejection_details=validation_result,
                task_spec=task_spec,
            )
            storage_service.store_session_response(session_id, response)
            return response

        # Step 3: Specialist Routing & Execution
        trace.add_step(
            component="SpecialistRouter",
            adapter_id="router_dispatch_v1.0",
            output_summary=f"Dispatched task '{task_spec.task_type.value}' to specialist models",
            parameters={"task_type": task_spec.task_type.value},
        )
        items, answer_text, boxes, region_tags = await self.specialist_router.route_and_execute(
            task_spec, images, session_id
        )

        # Step 4: Verifier Node
        trace.add_step(
            component="VerifierNode",
            adapter_id="spatial_consistency_verifier_v1.0",
            output_summary=f"Audited {len(boxes)} spatial features, geometry constraints, and cross-tool consistency",
        )
        geometry_ok, agreement_ok, qty_discrepancy, verifier_rationale = self.verifier_node.verify(
            task_spec, items
        )

        # Step 5: Confidence Scoring
        trace.add_step(
            component="ConfidenceScorer",
            adapter_id="bayesian_confidence_scorer_v1.0",
            output_summary="Calculated confidence tier based on verifier flags and sensor metadata",
        )
        confidence = self.confidence_scorer.compute(
            task_spec=task_spec,
            images=images,
            geometry_ok=geometry_ok,
            agreement_ok=agreement_ok,
            quantity_discrepancy=qty_discrepancy,
            verifier_rationale=verifier_rationale,
        )

        # Step 6: Response Assembly
        trace.add_step(
            component="ResponseComposer",
            output_summary="Assembled final grounded JSON payload with full audit trace",
        )
        execution_trace = trace.build_trace(
            selected_task_type=task_spec.task_type.value,
            confidence_tier=confidence.tier,
            confidence_rationale=confidence.rationale,
            rejection=None,
        )

        # Construct image preview URLs
        preview_urls = [img.preview_url for img in images if img.preview_url]

        response = AnalyzeResponse(
            session_id=session_id,
            answer_text=answer_text,
            evidence=EvidenceVisuals(
                boxes=boxes,
                masks=["mask_layer_01.png"] if any("change" in task_spec.task_type.value for _ in [1]) else [],
                region_tags=region_tags if region_tags else None,
                overlay_image_urls=preview_urls,
            ),
            confidence=confidence,
            execution_trace=execution_trace,
            report_url=f"/v1/session/{session_id}/report",
            rejected=False,
            rejection_reason=None,
            rejection_details=None,
            task_spec=task_spec,
        )

        storage_service.store_session_response(session_id, response)
        return response


orchestrator_service = OrchestratorService()
