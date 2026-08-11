"use client";

import { useCallback, useRef, useState } from "react";
import { ScanStatus } from "@/lib/types";

interface UploadPanelProps{
    status: ScanStatus;
    previewUrl: string | null;
    onFileSelected: (file:File) => void;
}

export default function UploadPanel({
    status,
    previewUrl,
    onFileSelected,
}: UploadPanelProps){
    const inputRef = useRef<HTMLInputElement>(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleFiles = useCallback(
        (files: FileList | null) =>{
            const file = files?.[0];
            if (file && file.type.startsWith("image/")){
                onFileSelected(file);

            }
        },
        [onFileSelected]
    );

    return(
        <div
      className={`relative aspect-[4/3] w-full overflow-hidden border transition-colors ${
        isDragging ? "border-cyan bg-cyan/5" : "border-cyan/30 bg-ink-deep/60"
      }`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFiles(e.dataTransfer.files);
      }}
    >
      <span className="corner-bracket left-3 top-3 border-l-2 border-t-2" />
      <span className="corner-bracket right-3 top-3 border-r-2 border-t-2" />
      <span className="corner-bracket bottom-3 left-3 border-b-2 border-l-2" />
      <span className="corner-bracket bottom-3 right-3 border-b-2 border-r-2" />

      {previewUrl ? (
        <img
          src={previewUrl}
          alt="Uploaded specimen"
          className="h-full w-full object-cover"
        />
      ) : (
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          className="flex h-full w-full flex-col items-center justify-center gap-3 px-8 text-center focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan"
        >
          <span className="font-mono text-xs uppercase tracking-[0.25em] text-cyan/70">
            No specimen loaded
          </span>
          <span className="max-w-[26ch] font-body text-sm text-off/70">
            Drop a photograph here, or click to select one from your device
          </span>
          <span className="mt-2 border border-cyan/40 px-4 py-2 font-mono text-xs uppercase tracking-widest text-cyan">
            Select image
          </span>
        </button>
      )}

      {status === "scanning" && (
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute inset-0 bg-ink/30" />
          <div className="absolute left-0 right-0 h-[2px] animate-scanline bg-cyan shadow-[0_0_12px_2px_rgba(111,214,232,0.8)]" />
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
    );
}