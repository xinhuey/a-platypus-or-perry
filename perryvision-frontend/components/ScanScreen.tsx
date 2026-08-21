"use client";

import {useState} from "react";
import UploadPanel from "./UploadPanel";
import SpecimenCard from "./SpecimenCard";
import { classifyImage } from "@/lib/classify";
import { ClassificationDisplay, ScanStatus } from "@/lib/types";
import { pickRandomGif } from "@/lib/gif";

export default function ScanScreen(){
    const [status, setStatus] = useState<ScanStatus>("idle");
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [result, setResult] = useState<ClassificationDisplay | null>(null);

    async function handleFileSelected(file:File){
        setPreviewUrl(URL.createObjectURL(file));
        setResult(null);
        setStatus("scanning");

        try{
            const classification = await classifyImage(file);
            setResult({
              ...classification,
              gifSrc: pickRandomGif(classification.verdict),
            });
            setStatus("done");
        }
        catch{
            setStatus("error");
        }
    }

    function reset(){
        setStatus("idle");
        setPreviewUrl(null);
        setResult(null);
    }

    return (
    <div className="grid w-full max-w-5xl grid-cols-1 gap-8 lg:grid-cols-[1.1fr_1fr] lg:items-start">
      <div>
        <UploadPanel
          status={status}
          previewUrl={previewUrl}
          onFileSelected={handleFileSelected}
        />
        <div className="mt-3 flex items-center justify-between font-mono text-[11px] uppercase tracking-widest text-off/40">
          <span>
            {status === "idle" && "Awaiting specimen"}
            {status === "scanning" && "Scan in progress…"}
            {status === "done" && "Scan complete"}
            {status === "error" && "Scan failed — try again"}
          </span>
          {previewUrl && (
            <button
              onClick={reset}
              className="underline decoration-dotted underline-offset-4 hover:text-cyan"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      <div className="lg:pt-2">
        {result ? (
          <SpecimenCard result={result} />
        ) : (
          <div className="flex h-full min-h-[220px] flex-col justify-center border border-dashed border-cyan/20 p-8 font-mono text-xs uppercase tracking-widest text-off/30">
            Results will be logged here once a specimen has been scanned.
          </div>
        )}
      </div>
    </div>
  );
}