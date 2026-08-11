export type Verdict = "agent" | "ordinary";

export interface ClassificationResult{
    verdict: Verdict;
    confidence: number; //0-1
    label: string;
    fieldNotes: string;
    gifSrc: string;

}

export type ScanStatus = "idle" | "scanning" | "done" | "error";