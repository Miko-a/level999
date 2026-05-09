"use client";

import { FormEvent, useEffect, useState } from "react";

type KnowledgeFile = {
  file_name: string;
  title: string;
  source_id: string;
  category: string;
  topic: string;
  version: string;
  size: number;
};

type VectorStats = {
  collection_name: string;
  chunk_count: number;
};

const API_BASE_URL = "http://127.0.0.1:8000";

export default function AdminPage() {
  const [files, setFiles] = useState<KnowledgeFile[]>([]);
  const [stats, setStats] = useState<VectorStats | null>(null);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [fileName, setFileName] = useState("");
  const [title, setTitle] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [category, setCategory] = useState("general");
  const [topic, setTopic] = useState("");
  const [version, setVersion] = useState("internal-demo");
  const [tags, setTags] = useState("");
  const [content, setContent] = useState("");

  async function loadFiles() {
    const response = await fetch(`${API_BASE_URL}/api/knowledge`);

    if (!response.ok) {
      throw new Error("Failed to load knowledge files.");
    }

    const data: { files: KnowledgeFile[] } = await response.json();
    setFiles(data.files);
  }

  async function loadStats() {
    const response = await fetch(`${API_BASE_URL}/api/knowledge/stats`);

    if (!response.ok) {
      throw new Error("Failed to load vector stats.");
    }

    const data: VectorStats = await response.json();
    setStats(data);
  }

  async function refreshData() {
    try {
      await Promise.all([loadFiles(), loadStats()]);
    } catch (error) {
      setMessage("Failed to refresh admin data.");
    }
  }

  useEffect(() => {
    refreshData();
  }, []);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!fileName.trim() || !title.trim() || !sourceId.trim() || !topic.trim() || !content.trim()) {
      setMessage("Please fill file name, title, source ID, topic, and content.");
      return;
    }

    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/knowledge`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          file_name: fileName,
          title,
          source_id: sourceId,
          category,
          topic,
          version,
          tags,
          content,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create knowledge file.");
      }

      setMessage(`Created: ${data.file_name}`);

      setFileName("");
      setTitle("");
      setSourceId("");
      setCategory("general");
      setTopic("");
      setVersion("internal-demo");
      setTags("");
      setContent("");

      await refreshData();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to create file.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleDelete(fileNameToDelete: string) {
    const confirmed = window.confirm(
      `Delete ${fileNameToDelete}? You must re-ingest after deleting.`
    );

    if (!confirmed) {
      return;
    }

    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/knowledge/${fileNameToDelete}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to delete file.");
      }

      setMessage(`Deleted: ${data.file_name}`);
      await refreshData();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to delete file.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleReingest() {
    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/knowledge/reingest`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to re-ingest knowledge base.");
      }

      setMessage(`Re-ingested ${data.chunk_count} chunks.`);
      await refreshData();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to re-ingest.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="mx-auto max-w-6xl px-4 py-6">
        <header className="mb-6 border-b border-slate-800 pb-4">
          <h1 className="text-2xl font-bold">HSR Knowledge Admin</h1>
          <p className="mt-2 text-sm text-slate-400">
            Manage local Markdown knowledge base and re-ingest vector database.
          </p>
        </header>

        <div className="mb-6 grid gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Markdown files
            </p>
            <p className="mt-2 text-2xl font-bold">{files.length}</p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Vector chunks
            </p>
            <p className="mt-2 text-2xl font-bold">
              {stats ? stats.chunk_count : "-"}
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Collection
            </p>
            <p className="mt-2 text-sm font-semibold">
              {stats ? stats.collection_name : "-"}
            </p>
          </div>
        </div>

        {message && (
          <div className="mb-6 rounded-xl border border-slate-700 bg-slate-900 p-4 text-sm text-slate-200">
            {message}
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
          <section className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <div className="mb-4 flex items-center justify-between gap-3">
              <h2 className="text-lg font-semibold">Knowledge Files</h2>

              <button
                onClick={handleReingest}
                disabled={isLoading}
                className="rounded-lg bg-blue-600 px-3 py-2 text-xs font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                Re-ingest
              </button>
            </div>

            <div className="space-y-3">
              {files.map((file) => (
                <div
                  key={file.file_name}
                  className="rounded-lg border border-slate-700 bg-slate-950 p-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-slate-100">
                        {file.title}
                      </p>
                      <p className="mt-1 text-xs text-slate-400">
                        {file.file_name}
                      </p>
                    </div>

                    <button
                      onClick={() => handleDelete(file.file_name)}
                      disabled={isLoading}
                      className="rounded-lg border border-red-900 px-2 py-1 text-xs text-red-300 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      Delete
                    </button>
                  </div>

                  <div className="mt-3 grid gap-2 text-xs text-slate-400">
                    <p>Source ID: {file.source_id}</p>
                    <p>
                      {file.category} / {file.topic}
                    </p>
                    <p>
                      Version: {file.version} | Size: {file.size} bytes
                    </p>
                  </div>
                </div>
              ))}

              {files.length === 0 && (
                <p className="text-sm text-slate-400">
                  No knowledge files found.
                </p>
              )}
            </div>
          </section>

          <section className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <h2 className="mb-4 text-lg font-semibold">Create Knowledge File</h2>

            <form onSubmit={handleCreate} className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <label className="block">
                  <span className="text-xs text-slate-400">File name</span>
                  <input
                    value={fileName}
                    onChange={(event) => setFileName(event.target.value)}
                    placeholder="break-effect-basics.md"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                  />
                </label>

                <label className="block">
                  <span className="text-xs text-slate-400">Title</span>
                  <input
                    value={title}
                    onChange={(event) => setTitle(event.target.value)}
                    placeholder="Break Effect Basics"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                  />
                </label>

                <label className="block">
                  <span className="text-xs text-slate-400">Source ID</span>
                  <input
                    value={sourceId}
                    onChange={(event) => setSourceId(event.target.value)}
                    placeholder="break-effect-basics"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                  />
                </label>

                <label className="block">
                  <span className="text-xs text-slate-400">Category</span>
                  <input
                    value={category}
                    onChange={(event) => setCategory(event.target.value)}
                    placeholder="combat"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                  />
                </label>

                <label className="block">
                  <span className="text-xs text-slate-400">Topic</span>
                  <input
                    value={topic}
                    onChange={(event) => setTopic(event.target.value)}
                    placeholder="break effect basics"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                  />
                </label>

                <label className="block">
                  <span className="text-xs text-slate-400">Version</span>
                  <input
                    value={version}
                    onChange={(event) => setVersion(event.target.value)}
                    placeholder="internal-demo"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                  />
                </label>
              </div>

              <label className="block">
                <span className="text-xs text-slate-400">Tags</span>
                <input
                  value={tags}
                  onChange={(event) => setTags(event.target.value)}
                  placeholder="break, toughness, weakness, beginner"
                  className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
                />
              </label>

              <label className="block">
                <span className="text-xs text-slate-400">Content</span>
                <textarea
                  value={content}
                  onChange={(event) => setContent(event.target.value)}
                  rows={14}
                  placeholder="Write the Markdown content here without the metadata header..."
                  className="mt-1 w-full resize-y rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm leading-relaxed outline-none focus:border-blue-500"
                />
              </label>

              <button
                type="submit"
                disabled={isLoading}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                Create File
              </button>
            </form>
          </section>
        </div>
      </section>
    </main>
  );
}