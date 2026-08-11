import { ClassificationResult } from "@/lib/types";

interface SpecimenCardProps{
    result: ClassificationResult;
}

export default function SpecimenCard({ result }: SpecimenCardProps){
    const isAgent = result.verdict === "agent";
    const stampColor = isAgent ? "text-alert border-alert" : "text-ink  border-ink";
    const stampText = isAgent ? "FLAGGED" : "CLEARED";

    return (
    <div className="paper-texture relative animate-fade-up border border-ink/10 p-6 text-ink shadow-[0_18px_40px_-12px_rgba(11,22,38,0.55)] sm:p-8">
      <div className="flex items-start justify-between gap-4 border-b border-ink/15 pb-4">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.3em] text-ink/50">
            Field Report No. {String(Date.now()).slice(-6)}
          </p>
          <h3 className="mt-1 font-display text-2xl italic text-ink">
            {isAgent ? "Case Reopened" : "Case Closed"}
          </h3>
        </div>
        <div
          className={`animate-stamp select-none rounded-sm border-[3px] px-3 py-1 font-mono text-xs font-medium uppercase tracking-widest ${stampColor}`}
          style={{ transform: "rotate(-8deg)" }}
        >
          {stampText}
        </div>
      </div>

      <dl className="mt-5 grid grid-cols-1 gap-3 font-mono text-xs sm:grid-cols-2">
        <div>
          <dt className="uppercase tracking-widest text-ink/45">Verdict</dt>
          <dd className="mt-1 text-sm text-ink">{result.label}</dd>
        </div>
        <div>
          <dt className="uppercase tracking-widest text-ink/45">Confidence</dt>
          <dd className="mt-1 flex items-center gap-2 text-sm text-ink">
            <span className="relative h-2 w-24 overflow-hidden rounded-full bg-ink/10">
              <span
                className={`absolute inset-y-0 left-0 ${
                  isAgent ? "bg-alert" : "bg-ink"
                }`}
                style={{ width: `${Math.round(result.confidence * 100)}%` }}
              />
            </span>
            {Math.round(result.confidence * 100)}%
          </dd>
        </div>
      </dl>

      <p className="mt-5 border-t border-dashed border-ink/20 pt-4 font-body text-sm leading-relaxed text-ink/80">
        {result.fieldNotes}
      </p>

      <div className="mt-5 overflow-hidden rounded-sm border border-ink/15 bg-ink-deep/5">
        <img 
        src={result.gifSrc}
          alt={isAgent ? "Agent identified reaction" : "Ordinary platypus reaction"}
          className="h-40 w-full object-cover"
          onError={(e) => {
            (e.target as HTMLImageElement).style.display = "none";
          }}
        />
      </div>
    </div>
  );
}