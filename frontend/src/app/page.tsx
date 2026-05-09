"use client";

import { FormEvent, useState } from "react";

type SourceDocument = {
  title: string;
  source_id: string;
  file_name: string;
  chunk_id: string;
  category: string;
  topic: string;
  version: string;
  score: number;
  preview: string;
};

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: SourceDocument[];
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Halo. Aku adalah HSR assistant. Saat ini aku memakai semantic retrieval dengan local vector database untuk mencari knowledge base yang relevan.",
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedInput = input.trim();

    if (!trimmedInput || isLoading) {
      return;
    }

    const userMessage: ChatMessage = {
      role: "user",
      content: trimmedInput,
    };

    setMessages((previousMessages) => [...previousMessages, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: trimmedInput,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from backend.");
      }

      const data: { answer: string; sources: SourceDocument[] } =
        await response.json();

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: data.answer,
        sources: data.sources,
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content:
          "Maaf, terjadi error saat menghubungi backend. Pastikan FastAPI berjalan di http://localhost:8000.",
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        errorMessage,
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="mx-auto flex min-h-screen max-w-4xl flex-col px-4 py-6">
        <header className="mb-6 border-b border-slate-800 pb-4">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold">
                HSR RAG Chatbot
              </h1>
              <p className="mt-2 text-sm text-slate-400">
                Ask anything related to Honkai Star Rail
              </p>
            </div>

            <a
              href="/admin/login"
              className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-blue-500 hover:text-white"
            >
              Admin
            </a>
          </div>
        </header>

        <div className="flex-1 space-y-4 overflow-y-auto rounded-xl border border-slate-800 bg-slate-900 p-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                  message.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-slate-800 text-slate-100"
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>

                {message.role === "assistant" &&
                  message.sources &&
                  message.sources.length > 0 && (
                    <div className="mt-4 border-t border-slate-700 pt-3">
                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                        Sources
                      </p>

                      <div className="space-y-2">
                        {message.sources.map((source, index) => (
                        <div
                          key={`${source.source_id}-${source.chunk_id}-${index}`}
                          className="rounded-lg border border-slate-700 bg-slate-900 p-3"
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div>
                              <p className="text-xs font-semibold text-slate-200">
                                {source.title}
                              </p>

                              <p className="mt-1 text-xs text-slate-400">
                                {source.category} / {source.topic}
                              </p>
                            </div>

                            <span className="rounded-full bg-slate-800 px-2 py-1 text-[10px] text-slate-400">
                              {source.score.toFixed(4)}
                            </span>
                          </div>

                          <p className="mt-2 text-xs text-slate-400">
                            File: {source.file_name}
                          </p>

                          <p className="mt-1 text-xs text-slate-400">
                            Chunk: {source.chunk_id} | Version: {source.version}
                          </p>

                          <p className="mt-2 text-xs text-slate-500">
                            {source.preview}
                          </p>
                        </div>
                      ))}
                      </div>
                    </div>
                  )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="rounded-xl bg-slate-800 px-4 py-3 text-sm text-slate-300">
                Thinking...
              </div>
            </div>
          )}
        </div>

        <form
          onSubmit={handleSubmit}
          className="mt-4 flex gap-3"
        >
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Tanya sesuatu tentang Honkai: Star Rail..."
            className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-100 outline-none focus:border-blue-500"
          />

          <button
            type="submit"
            disabled={isLoading}
            className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            Send
          </button>
        </form>
      </section>
    </main>
  );
}