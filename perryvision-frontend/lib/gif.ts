import { Verdict } from "./types";

const GIF_OPTIONS: Record<Verdict, string[]> = {
    agent:[
        "agent1.gif",
        "agent2.gif",
        "agent3.gif",
    ],
    ordinary:[
        "platy1.gif",
        "platy2.gif",
        "platy3.gif",
    ],
};

export function pickRandomGif(verdict: Verdict): string{
    const options = GIF_OPTIONS[verdict];
    const filename = options[Math.floor(Math.random() * options.length)];
    return `/gifs/${verdict}/${filename}`;
}