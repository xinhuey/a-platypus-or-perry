import ScanScreen from "@/components/ScanScreen";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center px-6 py-16 sm:py-24">
      <div className="mb-14 max-w-2xl text-center">
        <p className="font-mono text-xs uppercase tracking-[0.35em] text-cyan/70">
          Specimen Identification Terminal
        </p>
        <h1 className="mt-4 font-display text-4xl italic leading-tight text-off sm:text-5xl">
          Ordinary platypus,
          <br />
          or something else entirely?
        </h1>
        <p className="mx-auto mt-5 max-w-md font-body text-sm text-off/60">
          Upload a photograph below. The terminal will scan it against known
          field markers and return a verdict — something a certain evil
          scientist has never quite managed.
        </p>
      </div>

      <ScanScreen />

      <footer className="mt-20 font-mono text-[10px] uppercase tracking-[0.3em] text-off/25">
        Fan-made · Not affiliated with Disney · For educational use
      </footer>
    </main>
  );
}