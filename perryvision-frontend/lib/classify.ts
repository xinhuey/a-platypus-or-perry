import { ClassificationResult  } from "./types";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Sends the uploaded image to the backend classifier and returns a verdict.
 *
 * This is currently a placeholder that resolves with a mocked result so the
 * interface can be built and tested before the model/backend exists. Once
 * `backend/app.py` is running, replace the body of this function with a real
 * request, e.g.:
 *
 *   const form = new FormData();
 *   form.append("image", file);
 *   const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/classify`, {
 *     method: "POST",
 *     body: form,
 *   });
 *   if (!res.ok) throw new Error("Classification failed");
 *   return res.json();
 */

export async function classifyImage(
    file: File
): Promise<ClassificationResult>{
    await new Promise((resolve) => setTimeout(resolve, 1800));

    const isAgent = file.size % 2 === 0;

    if (isAgent){
        return{
            verdict: "agent",
            confidence: 0.94,
            label: "PERRY THE PLATYPUS??!!",
            fieldNotes:
                "A semi-aquatic agent in action",
            gifSrc: "/gifs/agent-result.gif",
        };
    }

    return{
        verdict: "ordinary",
            confidence: 0.88,
            label: "Relax. He's just a platypus",
            fieldNotes:
                "They don't do much.",
            gifSrc: "/gifs/ordinary-result.gif",
        };
}