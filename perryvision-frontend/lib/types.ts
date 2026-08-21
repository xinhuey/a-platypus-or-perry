export type Verdict = "agent" | "ordinary";

export interface ClassificationResult{
    verdict: Verdict;
    confidence: number; //0-1
    label: string;
    fieldNotes: string;
}

export interface ClassificationDisplay extends ClassificationResult{
    gifSrc: string;
}

export type ScanStatus = "idle" | "scanning" | "done" | "error";