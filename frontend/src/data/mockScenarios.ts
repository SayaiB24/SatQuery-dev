import type { DemoScenario } from '../types/satquery';

/**
 * High-definition synthetic satellite raster generators (SVG Data URIs)
 * Ensures 100% offline capability and crisp rendering during demos.
 */

export const OPTICAL_IMAGE_1 = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="%232d4a22"/>
      <stop offset="40%" stop-color="%233e5c2d"/>
      <stop offset="80%" stop-color="%235a783e"/>
    </linearGradient>
    <linearGradient id="water" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="%230f3854"/>
      <stop offset="100%" stop-color="%231e5c82"/>
    </linearGradient>
    <pattern id="urban" width="20" height="20" patternUnits="userSpaceOnUse">
      <rect width="18" height="18" fill="%23686868" opacity="0.6"/>
      <rect x="2" y="2" width="6" height="6" fill="%23a8a8a8"/>
      <rect x="10" y="10" width="6" height="6" fill="%238a4d3b"/>
    </pattern>
    <pattern id="fields" width="40" height="40" patternUnits="userSpaceOnUse">
      <rect width="38" height="38" fill="%23476326" opacity="0.7"/>
      <line x1="0" y1="10" x2="40" y2="10" stroke="%23334d16" stroke-width="2"/>
      <line x1="0" y1="25" x2="40" y2="25" stroke="%23334d16" stroke-width="2"/>
    </pattern>
  </defs>
  <rect width="600" height="400" fill="url(%23bg)"/>
  <!-- Field parcels -->
  <rect x="20" y="20" width="240" height="180" fill="url(%23fields)"/>
  <rect x="280" y="40" width="300" height="140" fill="%238b7d3a" opacity="0.6"/>
  <!-- Meandering River -->
  <path d="M 0,220 Q 150,180 280,260 T 600,240 L 600,290 Q 400,320 270,300 T 0,260 Z" fill="url(%23water)"/>
  <!-- Water Reservoir -->
  <ellipse cx="460" cy="110" rx="75" ry="45" fill="url(%23water)"/>
  <!-- Urban / Settlement zone -->
  <rect x="120" y="290" width="220" height="95" fill="url(%23urban)"/>
  <rect x="360" y="300" width="180" height="80" fill="url(%23urban)"/>
  <!-- Highway network -->
  <path d="M 230,0 L 250,400" stroke="%23d4d4d4" stroke-width="5" stroke-dasharray="8,2"/>
  <path d="M 0,160 Q 300,150 600,330" stroke="%23e5e5e5" stroke-width="4"/>
  <!-- Coordinate grid overlay -->
  <rect width="600" height="400" fill="none" stroke="%2338bdf8" stroke-width="1" opacity="0.3"/>
  <text x="20" y="30" fill="%23ffffff" font-family="monospace" font-size="12" opacity="0.8">OPTICAL [Cartosat-2S / S2] 0.65m GSD | BANDS: RGB-NIR</text>
</svg>`;

export const SAR_IMAGE_1 = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
  <defs>
    <linearGradient id="sar_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="%231a1a1a"/>
      <stop offset="100%" stop-color="%232b2b2b"/>
    </linearGradient>
    <filter id="speckle">
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" result="noise"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.45 0"/>
      <feComposite in2="SourceGraphic" in="gl" operator="in"/>
    </filter>
  </defs>
  <rect width="600" height="400" fill="url(%23sar_bg)"/>
  <!-- Speckle noise background -->
  <rect width="600" height="400" fill="%23444444" opacity="0.25"/>
  <!-- Water body has very low backscatter (dark specular reflection) -->
  <path d="M 0,220 Q 150,180 280,260 T 600,240 L 600,290 Q 400,320 270,300 T 0,260 Z" fill="%23050505"/>
  <ellipse cx="460" cy="110" rx="75" ry="45" fill="%23050505"/>
  <!-- Secondary hidden water body (visible in SAR, cloud covered in optical!) -->
  <ellipse cx="140" cy="90" rx="55" ry="32" fill="%23030303" stroke="%2338bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
  <!-- Double-bounce bright radar returns from urban buildings -->
  <rect x="120" y="290" width="220" height="95" fill="%23d6d6d6" opacity="0.85"/>
  <rect x="360" y="300" width="180" height="80" fill="%23e2e2e2" opacity="0.85"/>
  <!-- Highway reflection -->
  <path d="M 230,0 L 250,400" stroke="%23666666" stroke-width="4"/>
  <text x="20" y="30" fill="%2338bdf8" font-family="monospace" font-size="12" opacity="0.9">SAR [RISAT-1A / S1] C-Band VV/VH | BACKSCATTER dB</text>
  <text x="145" y="95" fill="%2338bdf8" font-family="sans-serif" font-size="11" font-weight="bold">SAR WATER DETECT (CLOUD PIERCED)</text>
</svg>`;

export const TEMPORAL_IMAGE_T1 = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
  <rect width="600" height="400" fill="%232b471e"/>
  <!-- Agricultural greenery everywhere in T1 -->
  <rect x="30" y="40" width="250" height="320" fill="%233d6b28" opacity="0.8"/>
  <rect x="320" y="40" width="240" height="180" fill="%23487a30" opacity="0.75"/>
  <!-- Small historic village -->
  <rect x="350" y="260" width="120" height="90" fill="%23737373"/>
  <circle cx="200" cy="180" r="40" fill="%231a4a6b"/>
  <text x="20" y="30" fill="%23ffffff" font-family="monospace" font-size="12">OBSERVATION T1 (2023-03-15) — PRE-DEVELOPMENT</text>
</svg>`;

export const TEMPORAL_IMAGE_T2 = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
  <rect width="600" height="400" fill="%232b471e"/>
  <!-- Retained greenery -->
  <rect x="30" y="40" width="250" height="320" fill="%233d6b28" opacity="0.8"/>
  <!-- CLEARED & BUILT EXPANSION in T2 -->
  <rect x="320" y="40" width="240" height="180" fill="%2394a3b8"/>
  <rect x="340" y="60" width="90" height="60" fill="%23e2e8f0"/>
  <rect x="450" y="80" width="80" height="70" fill="%23cbd5e1"/>
  <!-- Major Highway constructed -->
  <line x1="300" y1="0" x2="600" y2="400" stroke="%23475569" stroke-width="12"/>
  <line x1="300" y1="0" x2="600" y2="400" stroke="%23f8fafc" stroke-width="2" stroke-dasharray="6,4"/>
  <!-- Expanded village -->
  <rect x="350" y="240" width="210" height="130" fill="%2364748b"/>
  <circle cx="200" cy="180" r="40" fill="%231a4a6b"/>
  <text x="20" y="30" fill="%2338bdf8" font-family="monospace" font-size="12">OBSERVATION T2 (2025-01-20) — POST-DEVELOPMENT</text>
</svg>`;

export const DEMO_SCENARIOS: DemoScenario[] = [
  // Scenario A: Single-Image VQA
  {
    id: 'scenario_a',
    name: 'Scenario A: Single Scene Understanding',
    tag: 'Single-Image VQA',
    description: 'Analyze visual land-cover and dominant structures from a single high-resolution optical image.',
    query: 'Describe the land-cover and major objects visible in this image.',
    expectedTaskType: 'single_vqa',
    images: [
      {
        slot: 1,
        role: 'Primary Optical Scene',
        metadata: {
          imageId: 'img_opt_001',
          name: 'Cartosat2S_Scene_Bhopal.tif',
          format: 'geotiff',
          crs: 'EPSG:32643 (UTM Zone 43N)',
          bandCount: 4,
          detectedModality: 'optical',
          gsdMeters: 0.65,
          acquisitionTimestamp: '2024-11-04T05:32:10Z',
          nodataPercent: 0.0,
          cloudMaskPercent: 4.2,
          dimensions: { width: 1024, height: 1024 },
          previewUrl: OPTICAL_IMAGE_1
        }
      }
    ],
    mockResponse: {
      sessionId: 'sat-vqa-9014',
      answerText: 'The satellite scene exhibits a heterogeneous landscape dominated by managed agricultural parcels (46% area share) in the northern sectors, bisected by a natural meandering water drainage corridor (width 45–60 m). The southern portion contains a medium-density planned urban settlement with gridded asphalt road networks and commercial/residential structures. A major dual-lane transport highway traverses northwest to southeast.',
      evidence: {
        boxes: [
          { id: 'b1', label: 'Urban Settlement Zone', xLeft: 20, yTop: 72, xRight: 90, yBottom: 96, score: 0.94, isPrimary: true },
          { id: 'b2', label: 'Water Reservoir', xLeft: 64, yTop: 16, xRight: 88, yBottom: 38, score: 0.91, isPrimary: false },
          { id: 'b3', label: 'Agricultural Parcels', xLeft: 3, yTop: 5, xRight: 43, yBottom: 50, score: 0.88, isPrimary: false }
        ],
        masks: [],
        overlayImageUrls: [OPTICAL_IMAGE_1]
      },
      confidence: {
        tier: 'Medium',
        rationale: 'All geometric sanity checks verified within normalized coordinate bounds. Standard baseline confidence assigned for single-image open-ended descriptive VQA.',
        details: {
          geometryCheck: true,
          crossToolAgreement: true,
          quantityDiscrepancy: false
        }
      },
      executionTrace: {
        sessionId: 'sat-vqa-9014',
        selectedTaskType: 'single_vqa',
        confidenceTier: 'Medium',
        confidenceRationale: 'Single-image VQA baseline',
        steps: [
          {
            stepIndex: 1,
            component: 'query_interpreter',
            adapterIdOrVersion: null,
            parametersUsed: { query: 'Describe the land-cover...', intentConstraint: 'PS_TAXONOMY' },
            wallClockMs: 142,
            outputSummary: 'Parsed taskType: "single_vqa", intentConfidence: 0.96'
          },
          {
            stepIndex: 2,
            component: 'compatibility_validator',
            adapterIdOrVersion: null,
            parametersUsed: { imageCount: 1, modality: 'optical', format: 'geotiff', nodataPct: 0.0 },
            wallClockMs: 18,
            outputSummary: 'Precondition match: single optical GeoTIFF validated. All physical preconditions passed.'
          },
          {
            stepIndex: 3,
            component: 'specialist_router',
            adapterIdOrVersion: null,
            parametersUsed: { routingStrategy: 'deterministic_table' },
            wallClockMs: 5,
            outputSummary: 'Dispatched to specialist: vqa_caption_specialist'
          },
          {
            stepIndex: 4,
            component: 'vqa_caption_specialist',
            adapterIdOrVersion: 'adapter_vqa_caption:v1.2-lora',
            parametersUsed: { taskToken: '[vqa]', decoding: 'open_ended', maxTokens: 160 },
            wallClockMs: 840,
            outputSummary: 'Extracted scene description and classified 3 dominant LULC zones.'
          },
          {
            stepIndex: 5,
            component: 'verifier_node',
            adapterIdOrVersion: null,
            parametersUsed: { geometryCheck: true, bounds: '[0, 100]' },
            wallClockMs: 12,
            outputSummary: 'Geometric sanity passed: 3 bounding boxes validated inside raster boundaries.'
          },
          {
            stepIndex: 6,
            component: 'confidence_scorer',
            adapterIdOrVersion: null,
            parametersUsed: { decisionRule: 'rule_5_mvp_default' },
            wallClockMs: 6,
            outputSummary: 'Assigned tier "Medium" (MVP standard descriptive tier).'
          },
          {
            stepIndex: 7,
            component: 'response_composer',
            adapterIdOrVersion: null,
            parametersUsed: { citeSpecialists: true },
            wallClockMs: 75,
            outputSummary: 'Composed final evidence-grounded response.'
          }
        ]
      },
      reportUrl: '/v1/session/sat-vqa-9014/report?format=pdf',
      rejected: false,
      rejectionReason: null
    }
  },

  // Scenario B: Grounding with Ambiguity
  {
    id: 'scenario_b',
    name: 'Scenario B: Ambiguous Region Grounding',
    tag: 'Grounding Ambiguity',
    description: 'Test text-guided localization of geographic features with multi-candidate ambiguity handling.',
    query: 'Highlight the water body referred to in the query.',
    expectedTaskType: 'single_grounding',
    images: [
      {
        slot: 1,
        role: 'Primary Optical Scene',
        metadata: {
          imageId: 'img_opt_002',
          name: 'Sentinel2_Wetlands_Kerala.png',
          format: 'png',
          crs: 'EPSG:4326',
          bandCount: 3,
          detectedModality: 'optical',
          gsdMeters: 10.0,
          acquisitionTimestamp: '2024-09-18T04:45:00Z',
          nodataPercent: 0.0,
          dimensions: { width: 600, height: 400 },
          previewUrl: OPTICAL_IMAGE_1
        }
      }
    ],
    mockResponse: {
      sessionId: 'sat-grd-4421',
      answerText: 'Grounding query identified multiple plausible water bodies within the visual extent. Per SPDD §5.2 ambiguity protocol, both candidate referents have been surfaced: Candidate 1 corresponds to the primary artificial water reservoir in the north-east quadrant (88.4% confidence), while Candidate 2 corresponds to the natural meandering river basin traversing the central axis (74.1% confidence).',
      evidence: {
        boxes: [
          { id: 'box_cand_1', label: 'Candidate 1: Primary Reservoir (88.4%)', xLeft: 64, yTop: 16, xRight: 88, yBottom: 38, score: 0.884, isPrimary: true },
          { id: 'box_cand_2', label: 'Candidate 2: River Channel (74.1%)', xLeft: 2, yTop: 45, xRight: 98, yBottom: 75, score: 0.741, isPrimary: false }
        ],
        masks: [],
        overlayImageUrls: [OPTICAL_IMAGE_1]
      },
      confidence: {
        tier: 'Medium',
        rationale: 'Confidence discounted from High to Medium: multiple candidate referents detected for non-unique referent expression. Ambiguity handling triggered.',
        details: {
          geometryCheck: true,
          crossToolAgreement: true,
          quantityDiscrepancy: false
        }
      },
      executionTrace: {
        sessionId: 'sat-grd-4421',
        selectedTaskType: 'single_grounding',
        confidenceTier: 'Medium',
        confidenceRationale: 'Discounted due to multi-candidate ambiguity',
        steps: [
          {
            stepIndex: 1,
            component: 'query_interpreter',
            adapterIdOrVersion: null,
            parametersUsed: { query: 'Highlight the water body...' },
            wallClockMs: 110,
            outputSummary: 'Parsed taskType: "single_grounding", targetObject: "water body"'
          },
          {
            stepIndex: 2,
            component: 'compatibility_validator',
            adapterIdOrVersion: null,
            parametersUsed: { requiredModality: 'optical', format: 'png' },
            wallClockMs: 14,
            outputSummary: 'Passed input validation.'
          },
          {
            stepIndex: 3,
            component: 'grounding_specialist',
            adapterIdOrVersion: 'adapter_grounding:v1.0-lora',
            parametersUsed: { taskToken: '[ground]', topK: 5, threshold: 0.6 },
            wallClockMs: 910,
            outputSummary: 'Detected 2 candidates exceeding threshold. Flagged isAmbiguous=true.'
          },
          {
            stepIndex: 4,
            component: 'verifier_node',
            adapterIdOrVersion: null,
            parametersUsed: { verifyAllCandidates: true },
            wallClockMs: 15,
            outputSummary: 'All candidate coordinates conform to valid image bounds.'
          },
          {
            stepIndex: 5,
            component: 'confidence_scorer',
            adapterIdOrVersion: null,
            parametersUsed: { weakPointDiscount: 'non_unique_referent' },
            wallClockMs: 8,
            outputSummary: 'Applied 1-tier discount due to referent multiplicity.'
          },
          {
            stepIndex: 6,
            component: 'response_composer',
            adapterIdOrVersion: null,
            parametersUsed: {},
            wallClockMs: 60,
            outputSummary: 'Returned multi-candidate grounded visual evidence.'
          }
        ]
      },
      reportUrl: '/v1/session/sat-grd-4421/report?format=pdf',
      rejected: false,
      rejectionReason: null
    }
  },

  // Scenario C: Bi-Temporal Change Analysis
  {
    id: 'scenario_c',
    name: 'Scenario C: Bi-Temporal Urban Expansion',
    tag: 'Change Detection',
    description: 'Compare co-registered observations across two dates to identify spatial changes and verify quantities.',
    query: 'What changed between these two dates, and where did the change occur?',
    expectedTaskType: 'change_vqa',
    images: [
      {
        slot: 1,
        role: 'Observation T1 (Before)',
        metadata: {
          imageId: 'img_t1_2023',
          name: 'Sentinel2_Bengaluru_2023.tif',
          format: 'geotiff',
          crs: 'EPSG:32643',
          bandCount: 4,
          detectedModality: 'optical',
          gsdMeters: 10.0,
          acquisitionTimestamp: '2023-03-15T05:10:00Z',
          nodataPercent: 0.0,
          previewUrl: TEMPORAL_IMAGE_T1
        }
      },
      {
        slot: 2,
        role: 'Observation T2 (After)',
        metadata: {
          imageId: 'img_t2_2025',
          name: 'Sentinel2_Bengaluru_2025.tif',
          format: 'geotiff',
          crs: 'EPSG:32643',
          bandCount: 4,
          detectedModality: 'optical',
          gsdMeters: 10.0,
          acquisitionTimestamp: '2025-01-20T05:12:00Z',
          nodataPercent: 0.0,
          previewUrl: TEMPORAL_IMAGE_T2
        }
      }
    ],
    mockResponse: {
      sessionId: 'sat-chg-7782',
      answerText: 'Multitemporal change analysis reveals substantial urban and industrial expansion between March 2023 and January 2025. Approximately 38.4 hectares of former agricultural and scrub terrain in the eastern sector (upper-right quadrant) have been converted into built-up industrial plots and logistics facilities. A newly paved dual-carriageway arterial expressway has been laid diagonally across the landscape.',
      evidence: {
        boxes: [
          { id: 'chg_b1', label: 'New Industrial Hub (38.4 ha)', xLeft: 53, yTop: 10, xRight: 93, yBottom: 55, score: 0.96, isPrimary: true },
          { id: 'chg_b2', label: 'New Arterial Expressway', xLeft: 50, yTop: 0, xRight: 98, yBottom: 95, score: 0.92, isPrimary: false }
        ],
        masks: ['/evidence/mask_change_heatmap.png'],
        overlayImageUrls: [TEMPORAL_IMAGE_T2]
      },
      confidence: {
        tier: 'High',
        rationale: 'Geometric sanity verified within 88% spatial overlap; deterministic pixel change count (38.4 ha) matches model description within 2.1% error band.',
        details: {
          geometryCheck: true,
          crossToolAgreement: true,
          quantityDiscrepancy: false
        }
      },
      executionTrace: {
        sessionId: 'sat-chg-7782',
        selectedTaskType: 'change_vqa',
        confidenceTier: 'High',
        confidenceRationale: 'Passed geometric & deterministic pixel count cross-check',
        steps: [
          {
            stepIndex: 1,
            component: 'query_interpreter',
            adapterIdOrVersion: null,
            parametersUsed: { query: 'What changed between these two dates...' },
            wallClockMs: 130,
            outputSummary: 'Parsed taskType: "change_vqa", requiresTemporalPairing: true'
          },
          {
            stepIndex: 2,
            component: 'compatibility_validator',
            adapterIdOrVersion: null,
            parametersUsed: { count: 2, t1: '2023-03-15', t2: '2025-01-20', overlap: 0.88 },
            wallClockMs: 28,
            outputSummary: 'Validation passed: 2 optical images, valid temporal delta (677 days), 88% overlap.'
          },
          {
            stepIndex: 3,
            component: 'specialist_router',
            adapterIdOrVersion: null,
            parametersUsed: { routingTarget: 'change_vqa_specialist' },
            wallClockMs: 6,
            outputSummary: 'Dispatched to change_vqa_specialist'
          },
          {
            stepIndex: 4,
            component: 'change_vqa_specialist',
            adapterIdOrVersion: 'adapter_change_vqa:v1.1-cem',
            parametersUsed: { method: 'difference_attention_cem', quantityFlag: true },
            wallClockMs: 1240,
            outputSummary: 'Generated change description and calculated deterministicPixelCount = 3840 pixels (38.4 ha).'
          },
          {
            stepIndex: 5,
            component: 'verifier_node',
            adapterIdOrVersion: null,
            parametersUsed: { quantityTolerancePct: 15.0 },
            wallClockMs: 22,
            outputSummary: 'Deterministic quantity check PASSED: Model claim 38.4 ha vs pixel count 38.4 ha (0% discrepancy).'
          },
          {
            stepIndex: 6,
            component: 'confidence_scorer',
            adapterIdOrVersion: null,
            parametersUsed: { decisionRule: 'rule_4_high_confidence' },
            wallClockMs: 8,
            outputSummary: 'Assigned tier "High" (Clean verification & agreement).'
          },
          {
            stepIndex: 7,
            component: 'response_composer',
            adapterIdOrVersion: null,
            parametersUsed: {},
            wallClockMs: 85,
            outputSummary: 'Packaged temporal change evidence and generated trace.'
          }
        ]
      },
      reportUrl: '/v1/session/sat-chg-7782/report?format=pdf',
      rejected: false,
      rejectionReason: null
    }
  },

  // Scenario D: Optical-SAR Cross-Modal Fusion
  {
    id: 'scenario_d',
    name: 'Scenario D: Optical-SAR Complementary Fusion',
    tag: 'Optical-SAR Fusion',
    description: 'Extract complementary structural insights from co-registered Optical + Radar observations.',
    query: 'Use the optical and SAR images together to identify built-up and water-covered regions.',
    expectedTaskType: 'fusion',
    images: [
      {
        slot: 1,
        role: 'Optical Observation',
        metadata: {
          imageId: 'img_opt_s2',
          name: 'Sentinel2_RGBNIR_Assam.tif',
          format: 'geotiff',
          crs: 'EPSG:32646',
          bandCount: 4,
          detectedModality: 'optical',
          gsdMeters: 10.0,
          acquisitionTimestamp: '2024-07-12T04:20:00Z',
          nodataPercent: 0.0,
          cloudMaskPercent: 32.5,
          previewUrl: OPTICAL_IMAGE_1
        }
      },
      {
        slot: 2,
        role: 'SAR Observation',
        metadata: {
          imageId: 'img_sar_s1',
          name: 'Sentinel1_SAR_Assam_C_Band.tif',
          format: 'geotiff',
          crs: 'EPSG:32646',
          bandCount: 2,
          detectedModality: 'sar',
          gsdMeters: 10.0,
          acquisitionTimestamp: '2024-07-12T12:45:00Z',
          nodataPercent: 0.0,
          previewUrl: SAR_IMAGE_1
        }
      }
    ],
    mockResponse: {
      sessionId: 'sat-fus-5519',
      answerText: 'Joint Optical-SAR cross-modal analysis successfully extracted complementary signatures. Optical reflectance delineated bare soil boundaries and rural road connectivity. SAR microwave backscatter exhibited double-bounce scattering (VV/VH > -8 dB) verifying dense masonry settlements in the south. Critically, SAR C-band radar penetrated heavy cloud cover in the northwest to uncover an obscured 14.2-hectare retention water body undetectable in the optical spectrum alone.',
      evidence: {
        boxes: [
          { id: 'fus_b1', label: 'SAR-Uncovered Water (Cloud Pierced)', xLeft: 18, yTop: 14, xRight: 38, yBottom: 31, score: 0.94, isPrimary: true },
          { id: 'fus_b2', label: 'Dual-Sensor Confirmed Urban Zone', xLeft: 20, yTop: 72, xRight: 90, yBottom: 96, score: 0.97, isPrimary: false }
        ],
        masks: [],
        regionTags: [
          { region: 'Northwest Basin', tag: 'sar_only', score: 0.94, description: 'Detected via SAR specular reflection through heavy optical cloud cover' },
          { region: 'Southern Settlement', tag: 'agreement', score: 0.97, description: 'Corroborated by optical spectral signature and SAR double-bounce backscatter' },
          { region: 'Eastern Field Parcels', tag: 'optical_only', score: 0.82, description: 'Agricultural texture visible optically; SAR backscatter diffuse' }
        ],
        overlayImageUrls: [OPTICAL_IMAGE_1, SAR_IMAGE_1]
      },
      confidence: {
        tier: 'High',
        rationale: 'Co-registered footprint overlap 94%; complementarity detector confirmed dual-sensor agreement on built-up zones with reliable SAR-only hydrological identification.',
        details: {
          geometryCheck: true,
          crossToolAgreement: true,
          quantityDiscrepancy: false
        }
      },
      executionTrace: {
        sessionId: 'sat-fus-5519',
        selectedTaskType: 'fusion',
        confidenceTier: 'High',
        confidenceRationale: 'High multi-sensor complementarity and overlap',
        steps: [
          {
            stepIndex: 1,
            component: 'query_interpreter',
            adapterIdOrVersion: null,
            parametersUsed: { query: 'Use optical and SAR images together...' },
            wallClockMs: 125,
            outputSummary: 'Parsed taskType: "fusion", requiredModalities: ["optical", "sar"]'
          },
          {
            stepIndex: 2,
            component: 'compatibility_validator',
            adapterIdOrVersion: null,
            parametersUsed: { pairType: 'cross_modal', overlap: 0.94, crsCheck: 'PASS' },
            wallClockMs: 25,
            outputSummary: 'Validation PASSED: 1 Optical + 1 SAR image, co-registered CRS, 94% spatial overlap.'
          },
          {
            stepIndex: 3,
            component: 'specialist_router',
            adapterIdOrVersion: null,
            parametersUsed: { routingTarget: 'fusion_pipeline' },
            wallClockMs: 7,
            outputSummary: 'Dispatched to 3-stage fusion_pipeline'
          },
          {
            stepIndex: 4,
            component: 'fusion_pipeline.evidence_extraction',
            adapterIdOrVersion: 'adapter_vqa_caption:v1.2-lora',
            parametersUsed: { passes: 2, modalities: ['optical', 'sar'] },
            wallClockMs: 950,
            outputSummary: 'Extracted independent structured evidence from optical and SAR scenes.'
          },
          {
            stepIndex: 5,
            component: 'fusion_pipeline.complementarity_detector',
            adapterIdOrVersion: 'infonce_alignment_weights:v1.0',
            parametersUsed: { threshold: 0.75 },
            wallClockMs: 180,
            outputSummary: 'Tagged regions: 1 agreement (urban), 1 sar_only (cloud-penetrated water), 1 optical_only (fields).'
          },
          {
            stepIndex: 6,
            component: 'fusion_pipeline.verbalizer',
            adapterIdOrVersion: 'controller_llm:frozen_decoder',
            parametersUsed: { modalityCitation: true },
            wallClockMs: 310,
            outputSummary: 'Synthesized grounded answer citing specific sensors for each geographical claim.'
          },
          {
            stepIndex: 7,
            component: 'verifier_node',
            adapterIdOrVersion: null,
            parametersUsed: { crossToolAgreement: 'high' },
            wallClockMs: 14,
            outputSummary: 'Verified cross-modal agreement score > 0.85.'
          },
          {
            stepIndex: 8,
            component: 'confidence_scorer',
            adapterIdOrVersion: null,
            parametersUsed: { rule: 'rule_4_high' },
            wallClockMs: 6,
            outputSummary: 'Assigned tier "High".'
          }
        ]
      },
      reportUrl: '/v1/session/sat-fus-5519/report?format=pdf',
      rejected: false,
      rejectionReason: null
    }
  },

  // Scenario E: Compound Workflow (Fusion -> Change)
  {
    id: 'scenario_e',
    name: 'Scenario E: Compound Workflow (Fusion → Change)',
    tag: 'Compound Sequential Plan',
    description: 'Execute multi-step sequential reasoning: First identify infrastructure via fusion, then evaluate expansion.',
    query: 'Use the optical and SAR images together to identify built-up areas, then determine whether the built-up area increased.',
    expectedTaskType: 'fusion_then_change',
    images: [
      {
        slot: 1,
        role: 'Optical Scene',
        metadata: {
          imageId: 'img_comp_opt',
          name: 'Cartosat2S_Hyderabad.tif',
          format: 'geotiff',
          crs: 'EPSG:32644',
          bandCount: 4,
          detectedModality: 'optical',
          gsdMeters: 0.65,
          nodataPercent: 0.0,
          previewUrl: OPTICAL_IMAGE_1
        }
      },
      {
        slot: 2,
        role: 'SAR Scene',
        metadata: {
          imageId: 'img_comp_sar',
          name: 'RISAT1_Hyderabad_DualPol.tif',
          format: 'geotiff',
          crs: 'EPSG:32644',
          bandCount: 2,
          detectedModality: 'sar',
          gsdMeters: 1.0,
          nodataPercent: 0.0,
          previewUrl: SAR_IMAGE_1
        }
      }
    ],
    mockResponse: {
      sessionId: 'sat-cmp-8812',
      answerText: 'Step 1 (Fusion Analysis): Optical and SAR fusion confirmed 62.4 hectares of high-density built-up structures with active construction on the eastern fringe. Step 2 (Temporal Change Assessment): Note that computing an empirical rate of increase requires a historical baseline image; however, based on unpaved foundation scarring visible in the optical data and high corner-reflector SAR scatter, active expansion is ongoing along the southern corridor.',
      evidence: {
        boxes: [
          { id: 'cmp_b1', label: 'Confirmed Built-Up Cluster (Fusion)', xLeft: 20, yTop: 72, xRight: 90, yBottom: 96, score: 0.95, isPrimary: true },
          { id: 'cmp_b2', label: 'Active Construction Fringe', xLeft: 60, yTop: 75, xRight: 90, yBottom: 95, score: 0.88, isPrimary: false }
        ],
        masks: [],
        regionTags: [
          { region: 'Core Urban Zone', tag: 'agreement', score: 0.96 },
          { region: 'Expansion Boundary', tag: 'optical_only', score: 0.84 }
        ],
        overlayImageUrls: [OPTICAL_IMAGE_1]
      },
      confidence: {
        tier: 'Medium',
        rationale: 'Compound workflow executed successfully across 2 specialist stages. Confidence tiered to Medium due to missing historical baseline observation.',
        details: {
          geometryCheck: true,
          crossToolAgreement: true,
          quantityDiscrepancy: false
        }
      },
      executionTrace: {
        sessionId: 'sat-cmp-8812',
        selectedTaskType: 'fusion_then_change',
        confidenceTier: 'Medium',
        confidenceRationale: 'Compound sequential plan completed with temporal data caveat',
        steps: [
          {
            stepIndex: 1,
            component: 'query_interpreter',
            adapterIdOrVersion: null,
            parametersUsed: { query: 'Use optical and SAR... then determine increase' },
            wallClockMs: 155,
            outputSummary: 'Parsed compound task: "fusion_then_change", requiresSequencing: true'
          },
          {
            stepIndex: 2,
            component: 'compatibility_validator',
            adapterIdOrVersion: null,
            parametersUsed: { suppliedCount: 2, expectedForFullChange: 3 },
            wallClockMs: 25,
            outputSummary: 'Validation warning: 2 images supplied for compound query. Proceeding with spatial fusion and active expansion assessment.'
          },
          {
            stepIndex: 3,
            component: 'specialist_router',
            adapterIdOrVersion: null,
            parametersUsed: { sequence: ['fusion_pipeline', 'change_vqa_specialist'] },
            wallClockMs: 10,
            outputSummary: 'Generated sequential plan: 1. fusion_pipeline -> 2. change_vqa_specialist'
          },
          {
            stepIndex: 4,
            component: 'fusion_pipeline',
            adapterIdOrVersion: 'composite_adapter',
            parametersUsed: { subSteps: 3 },
            wallClockMs: 1120,
            outputSummary: 'Extracted fused built-up footprint (62.4 ha).'
          },
          {
            stepIndex: 5,
            component: 'change_vqa_specialist',
            adapterIdOrVersion: 'adapter_change_vqa:v1.1-cem',
            parametersUsed: { inputContext: 'fusion_footprint' },
            wallClockMs: 780,
            outputSummary: 'Evaluated expansion perimeter and identified active earthwork scarring.'
          },
          {
            stepIndex: 6,
            component: 'verifier_node',
            adapterIdOrVersion: null,
            parametersUsed: { multiStageCheck: true },
            wallClockMs: 20,
            outputSummary: 'All intermediate outputs verified against geographic constraints.'
          },
          {
            stepIndex: 7,
            component: 'confidence_scorer',
            adapterIdOrVersion: null,
            parametersUsed: { discount: 'missing_temporal_baseline' },
            wallClockMs: 8,
            outputSummary: 'Set tier "Medium" with transparent data caveat.'
          },
          {
            stepIndex: 8,
            component: 'response_composer',
            adapterIdOrVersion: null,
            parametersUsed: {},
            wallClockMs: 95,
            outputSummary: 'Composed multi-stage answer citing both specialists in sequence.'
          }
        ]
      },
      reportUrl: '/v1/session/sat-cmp-8812/report?format=pdf',
      rejected: false,
      rejectionReason: null
    }
  },

  // Scenario F: Input Compatibility Rejection (First-Class Rejection Demo)
  {
    id: 'scenario_f',
    name: 'Scenario F: Physical Input Mismatch (Rejection Demo)',
    tag: 'Input Validation Rejection',
    description: 'Demonstrate first-class precondition checking: Requesting temporal change on an Optical-SAR pair.',
    query: 'What changed between these two dates and did built-up area increase?',
    expectedTaskType: 'change_vqa',
    images: [
      {
        slot: 1,
        role: 'Optical Image',
        metadata: {
          imageId: 'img_rej_opt',
          name: 'Optical_Sensor_Scene.png',
          format: 'png',
          crs: 'EPSG:4326',
          bandCount: 3,
          detectedModality: 'optical',
          gsdMeters: 5.0,
          nodataPercent: 0.0,
          previewUrl: OPTICAL_IMAGE_1
        }
      },
      {
        slot: 2,
        role: 'SAR Image',
        metadata: {
          imageId: 'img_rej_sar',
          name: 'SAR_Radar_Scene.png',
          format: 'png',
          crs: 'EPSG:4326',
          bandCount: 1,
          detectedModality: 'sar',
          gsdMeters: 5.0,
          nodataPercent: 0.0,
          previewUrl: SAR_IMAGE_1
        }
      }
    ],
    mockResponse: {
      sessionId: 'sat-rej-1029',
      answerText: null,
      evidence: {
        boxes: [],
        masks: [],
        overlayImageUrls: []
      },
      confidence: {
        tier: 'Low',
        rationale: 'Precondition validation failed prior to specialist execution.'
      },
      executionTrace: {
        sessionId: 'sat-rej-1029',
        selectedTaskType: 'change_vqa',
        confidenceTier: 'Low',
        confidenceRationale: 'Physical precondition mismatch',
        rejection: {
          reasonCode: 'modality_mismatch',
          humanReadableReason: 'Multitemporal change analysis requires two spatially corresponding observations of the SAME sensor modality acquired at different dates. You have supplied 1 Optical image and 1 SAR radar image, which constitutes a cross-modal pair rather than a bi-temporal change pair.',
          suggestedAction: 'To analyze temporal change, upload before (T1) and after (T2) images from the same sensor. If you wish to analyze the current pair, change your query to an Optical-SAR fusion query (e.g. "Use optical and SAR together to identify water bodies").',
          detectedContext: {
            'Image 1 Detected Modality': 'Optical (RGB / Multispectral)',
            'Image 2 Detected Modality': 'SAR (Synthetic Aperture Radar)'
          },
          requiredContext: {
            'Required for Change Analysis': 'Two images of identical modality (Optical+Optical OR SAR+SAR) with distinct acquisition timestamps'
          }
        },
        steps: [
          {
            stepIndex: 1,
            component: 'query_interpreter',
            adapterIdOrVersion: null,
            parametersUsed: { query: 'What changed between these two dates...' },
            wallClockMs: 118,
            outputSummary: 'Interpreted intent: "change_vqa" (requires same-modality temporal pair).'
          },
          {
            stepIndex: 2,
            component: 'compatibility_validator',
            adapterIdOrVersion: null,
            parametersUsed: {
              modality1: 'optical',
              modality2: 'sar',
              required: 'same_modality'
            },
            wallClockMs: 16,
            status: 'rejected',
            outputSummary: 'REJECTED: Precondition check failed with reason code "modality_mismatch". Execution halted.'
          }
        ]
      },
      reportUrl: null,
      rejected: true,
      rejectionReason: 'Multitemporal change analysis requires two spatially corresponding observations of the SAME sensor modality acquired at different dates.',
      rejectionDetails: {
        reasonCode: 'modality_mismatch',
        humanReadableReason: 'Multitemporal change analysis requires two spatially corresponding observations of the SAME sensor modality acquired at different dates. You have supplied 1 Optical image and 1 SAR radar image, which constitutes a cross-modal pair rather than a bi-temporal change pair.',
        suggestedAction: 'To analyze temporal change, upload before (T1) and after (T2) images from the same sensor. If you wish to analyze the current pair, change your query to an Optical-SAR fusion query (e.g. "Use optical and SAR together to identify water bodies").',
        detectedContext: {
          'Image 1 Detected Modality': 'Optical (RGB / Multispectral)',
          'Image 2 Detected Modality': 'SAR (Synthetic Aperture Radar)'
        },
        requiredContext: {
          'Required for Change Analysis': 'Two images of identical modality (Optical+Optical OR SAR+SAR) with distinct acquisition timestamps'
        }
      }
    }
  }
];
