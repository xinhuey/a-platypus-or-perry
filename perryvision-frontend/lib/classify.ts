import { ClassificationResult  } from "./types";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Sends the uploaded image to the backend classifier and returns a verdict.
 *
 * 
 */

export async function classifyImage(
    file: File
): Promise<ClassificationResult>{
    const form = new FormData();
    form.append("image", file);

    const res = await fetch(`${API_URL}/classify`, {
        method: "POST",
        body: form,
    });

    if (!res.ok){
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || "Classification failed");
    }

    return res.json();
}