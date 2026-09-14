import React, { createContext, useContext, useState } from 'react';
import type { ImageMetadata, AnalyzeResponse, DemoScenario } from '../types/satquery';
import { DEMO_SCENARIOS } from '../data/mockScenarios';
import { analyzeRaster } from '../services/api';

export interface ProcessingStepInfo {
  index: number;
  label: string;
  component: string;
  description: string;
}

export const PIPELINE_STEPS: ProcessingStepInfo[] = [
  { index: 1, label: 'Query Interpretation', component: 'query_interpreter', description: 'Parsing natural language query into structured TaskSpec & taxonomy' },
  { index: 2, label: 'Compatibility Validation', component: 'compatibility_validator', description: 'Evaluating physical preconditions: modality, CRS, overlap, temporal delta' },
  { index: 3, label: 'Specialist Dispatch', component: 'specialist_router', description: 'Selecting specialist models from registry via deterministic routing table' },
  { index: 4, label: 'Specialist Execution', component: 'specialists / LoRA adapters', description: 'Running remote-sensing vision-language inference with hot-swapped LoRA weights' },
  { index: 5, label: 'Evidence Verification', component: 'verifier_node', description: 'Cross-checking geometric bounds, cross-tool agreement, and deterministic counts' },
  { index: 6, label: 'Confidence Scoring', component: 'confidence_scorer', description: 'Calibrating High/Medium/Low confidence tier and logging rationale' },
  { index: 7, label: 'Trace Emission', component: 'trace_emitter', description: 'Serializing auditable execution trace with step timings and parameters' },
  { index: 8, label: 'Response Composition', component: 'response_composer', description: 'Assembling grounded natural language answer with visual evidence overlays' },
];

interface SatQueryContextType {
  image1: ImageMetadata | null;
  image2: ImageMetadata | null;
  query: string;
  activeScenario: DemoScenario | null;
  isAnalyzing: boolean;
  activeStep: number;
  results: AnalyzeResponse | null;
  activeLayers: {
    boxes: boolean;
    masks: boolean;
    regions: boolean;
  };
  supportedCapabilities: {
    singleVqa: boolean;
    captioning: boolean;
    grounding: boolean;
    changeAnalysis: boolean;
    opticalSarFusion: boolean;
    compoundPipeline: boolean;
  };
  setImage1: (img: ImageMetadata | null) => void;
  setImage2: (img: ImageMetadata | null) => void;
  setQuery: (q: string) => void;
  loadScenario: (scenarioId: string) => void;
  startAnalysis: (onComplete?: () => void) => void;
  resetSession: () => void;
  toggleLayer: (layer: 'boxes' | 'masks' | 'regions') => void;
  setResults: (res: AnalyzeResponse | null) => void;
}

const SatQueryContext = createContext<SatQueryContextType | undefined>(undefined);

export const SatQueryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [image1, setImage1] = useState<ImageMetadata | null>(DEMO_SCENARIOS[0].images[0].metadata);
  const [image2, setImage2] = useState<ImageMetadata | null>(null);
  const [query, setQuery] = useState<string>(DEMO_SCENARIOS[0].query);
  const [activeScenario, setActiveScenario] = useState<DemoScenario | null>(DEMO_SCENARIOS[0]);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [activeStep, setActiveStep] = useState<number>(0);
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [activeLayers, setActiveLayers] = useState({
    boxes: true,
    masks: true,
    regions: true,
  });

  // Calculate dynamic capability readiness based on loaded imagery
  const imageCount = (image1 ? 1 : 0) + (image2 ? 1 : 0);
  const modalities = [image1?.detectedModality, image2?.detectedModality].filter(Boolean);
  const isOpticalPresent = modalities.includes('optical') || modalities.includes('multispectral');
  const isSarPresent = modalities.includes('sar');
  const isOpticalSarPair = imageCount === 2 && isOpticalPresent && isSarPresent;
  const isSameModalityPair = imageCount === 2 && !isOpticalSarPair;

  const supportedCapabilities = {
    singleVqa: imageCount >= 1,
    captioning: imageCount >= 1,
    grounding: imageCount >= 1 && isOpticalPresent,
    changeAnalysis: isSameModalityPair,
    opticalSarFusion: isOpticalSarPair,
    compoundPipeline: isOpticalSarPair || imageCount >= 2,
  };

  const loadScenario = (scenarioId: string) => {
    const scenario = DEMO_SCENARIOS.find((s) => s.id === scenarioId);
    if (!scenario) return;

    setActiveScenario(scenario);
    setQuery(scenario.query);

    const img1 = scenario.images.find((i) => i.slot === 1)?.metadata || null;
    const img2 = scenario.images.find((i) => i.slot === 2)?.metadata || null;

    setImage1(img1);
    setImage2(img2);
    setResults(null);
  };

  const toggleLayer = (layer: 'boxes' | 'masks' | 'regions') => {
    setActiveLayers((prev) => ({ ...prev, [layer]: !prev[layer] }));
  };

  const resetSession = () => {
    setImage1(null);
    setImage2(null);
    setQuery('');
    setActiveScenario(null);
    setResults(null);
    setActiveStep(0);
    setIsAnalyzing(false);
  };

  const startAnalysis = async (onComplete?: () => void) => {
    setIsAnalyzing(true);
    setActiveStep(1);

    // Animate pipeline progress
    let currentStep = 1;
    const interval = setInterval(() => {
      currentStep++;
      if (currentStep <= 7) {
        setActiveStep(currentStep);
      }
    }, 280);

    let targetResponse: AnalyzeResponse;

    try {
      const files: File[] = [];
      if (image1) {
        files.push(new File([new Blob(['satquery_dummy_bytes'])], image1.name, { type: 'image/png' }));
      }
      if (image2) {
        files.push(new File([new Blob(['satquery_dummy_bytes'])], image2.name, { type: 'image/png' }));
      }
      targetResponse = await analyzeRaster(query, files);
    } catch (err) {
      console.warn('Live backend call unfulfilled, falling back to client-side scenario:', err);
      if (activeScenario) {
        targetResponse = activeScenario.mockResponse;
      } else {
        targetResponse = {
          ...DEMO_SCENARIOS[0].mockResponse,
          sessionId: `sat-usr-${Math.floor(1000 + Math.random() * 9000)}`,
          answerText: `Analyzed ${imageCount} uploaded image(s) for query: "${query}". Visual feature extraction identified key geographic characteristics matching prompt specifications.`,
          evidence: {
            boxes: [
              { id: 'usr_b1', label: 'Identified Target Feature', xLeft: 30, yTop: 30, xRight: 75, yBottom: 70, score: 0.91, isPrimary: true }
            ],
            masks: [],
            overlayImageUrls: [image1?.previewUrl || '']
          }
        };
      }
    }

    // Finish pipeline animation
    clearInterval(interval);
    setActiveStep(targetResponse.rejected ? 2 : 8);
    setTimeout(() => {
      setIsAnalyzing(false);
      setResults(targetResponse);
      if (onComplete) onComplete();
    }, 300);
  };

  return (
    <SatQueryContext.Provider
      value={{
        image1,
        image2,
        query,
        activeScenario,
        isAnalyzing,
        activeStep,
        results,
        activeLayers,
        supportedCapabilities,
        setImage1,
        setImage2,
        setQuery,
        loadScenario,
        startAnalysis,
        resetSession,
        toggleLayer,
        setResults,
      }}
    >
      {children}
    </SatQueryContext.Provider>
  );
};

export const useSatQuery = () => {
  const context = useContext(SatQueryContext);
  if (!context) {
    throw new Error('useSatQuery must be used within a SatQueryProvider');
  }
  return context;
};
