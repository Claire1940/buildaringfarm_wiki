"use client";

import { useMemo, useState } from "react";
import Image from "next/image";
import { ExternalLink, Play } from "lucide-react";

interface VideoFeatureProps {
  videoId: string;
  title: string;
  posterImage: string;
}

export function VideoFeature({
  videoId,
  title,
  posterImage,
}: VideoFeatureProps) {
  const [isPlaying, setIsPlaying] = useState(false);

  const watchUrl = useMemo(
    () => `https://www.youtube.com/watch?v=${videoId}`,
    [videoId],
  );

  const embedUrl = useMemo(
    () =>
      `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&playsinline=1&rel=0`,
    [videoId],
  );

  const handlePlay = () => {
    setIsPlaying(true);
  };

  return (
    <div className="space-y-4">
      <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
        {!isPlaying ? (
          <>
            <Image
              src={posterImage}
              alt={title}
              fill
              className="object-cover rounded-lg"
              priority
            />
            <button
              type="button"
              aria-label={`Play ${title}`}
              className="absolute inset-0 flex items-center justify-center bg-black/30 hover:bg-black/40 transition-colors cursor-pointer rounded-lg"
              onClick={handlePlay}
            >
              <div className="w-16 h-16 md:w-20 md:h-20 bg-[hsl(var(--nav-theme))] hover:bg-[hsl(var(--nav-theme-light))] rounded-full flex items-center justify-center transition-colors">
                <Play
                  className="w-8 h-8 md:w-10 md:h-10 text-white ml-1"
                  fill="white"
                />
              </div>
            </button>
          </>
        ) : (
          <iframe
            className="absolute top-0 left-0 w-full h-full rounded-lg"
            src={embedUrl}
            title={title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          />
        )}
      </div>

      <div className="flex justify-center">
        <a
          href={watchUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium text-muted-foreground hover:bg-white/10 hover:text-foreground transition-colors"
        >
          Watch on YouTube
          <ExternalLink className="h-4 w-4" />
        </a>
      </div>
    </div>
  );
}
