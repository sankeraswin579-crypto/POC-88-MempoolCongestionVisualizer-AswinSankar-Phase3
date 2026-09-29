"use client";

import { FormEvent, useState } from "react";

type AssistantResponse = {
  answer_id: string;
  status: "answered" | "unsupported" | "unsafe" | "unavailable" | "error";
  intent?: string | null;
  answer: string;
  evidence_references: string[];
  key_values: Array<{
    name: string;
    value: unknown;
    unit?: string;
  }>;
  metadata: {
    data_version?: string;
    method_version?: string | string[];
    quality_status?: string;
  };
  limitation?: string;
  suggested_follow_ups?: string[];
};

const SUGGESTED_QUESTIONS = [
  "What is the baseline for transaction count?",
  "What is the range for block size?",
  "What is the highest observed block weight?",
  "What is the approved comparative method?",
  "What are the limitations of this analysis?",
];

export default function GroundedAssistant() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] =
    useState<AssistantResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submitQuestion(event: FormEvent) {
    event.preventDefault();

    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const result = await fetch("/api/assistant/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      if (!result.ok) {
        throw new Error(
          `Assistant request failed: ${result.status}`
        );
      }

      const data =
        (await result.json()) as AssistantResponse;

      setResponse(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to contact the grounded assistant."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-2xl border bg-white p-6 shadow-sm">
      <div>
        <p className="text-sm font-medium uppercase tracking-wide text-blue-600">
          Phase 3 Post #5
        </p>

        <h2 className="mt-1 text-2xl font-bold">
          Grounded Data Assistant
        </h2>

        <p className="mt-2 max-w-3xl text-sm text-gray-600">
          Ask questions about the approved Track A comparative
          evidence. Responses are generated from deterministic
          Phase 3 results and include traceable evidence metadata.
        </p>
      </div>

      <form
        onSubmit={submitQuestion}
        className="mt-5 flex flex-col gap-3 sm:flex-row"
      >
        <input
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          maxLength={500}
          placeholder="Ask about an approved comparative result..."
          className="flex-1 rounded-lg border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-200"
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="rounded-lg bg-blue-700 px-5 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Checking..." : "Ask"}
        </button>
      </form>

      <div className="mt-4 flex flex-wrap gap-2">
        {SUGGESTED_QUESTIONS.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => setQuestion(item)}
            className="rounded-full border px-3 py-2 text-xs text-gray-700 hover:bg-gray-50"
          >
            {item}
          </button>
        ))}
      </div>

      {error && (
        <div className="mt-5 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          {error}
        </div>
      )}

      {response && (
        <div className="mt-6 rounded-xl border bg-gray-50 p-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full border px-3 py-1 text-xs font-semibold">
              {response.status}
            </span>

            {response.intent && (
              <span className="rounded-full border px-3 py-1 text-xs text-gray-600">
                {response.intent}
              </span>
            )}
          </div>

          <div className="mt-4">
            <h3 className="font-semibold">
              Grounded answer
            </h3>

            <p className="mt-2 text-sm leading-6 text-gray-700">
              {response.answer}
            </p>
          </div>

          {response.key_values.length > 0 && (
            <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {response.key_values.map((item) => (
                <div
                  key={item.name}
                  className="rounded-lg border bg-white p-3"
                >
                  <p className="text-xs uppercase tracking-wide text-gray-500">
                    {item.name.replaceAll("_", " ")}
                  </p>

                  <p className="mt-1 font-semibold">
                    {String(item.value)}
                    {item.unit ? ` ${item.unit}` : ""}
                  </p>
                </div>
              ))}
            </div>
          )}

          <div className="mt-5 rounded-lg border bg-white p-4">
            <h3 className="text-sm font-semibold">
              Traceability
            </h3>

            <div className="mt-2 space-y-1 text-xs text-gray-600">
              <p>
                Data version:{" "}
                {response.metadata.data_version ?? "N/A"}
              </p>

              <p>
                Method version:{" "}
                {Array.isArray(
                  response.metadata.method_version
                )
                  ? response.metadata.method_version.join(", ")
                  : response.metadata.method_version ?? "N/A"}
              </p>

              <p>
                Quality:{" "}
                {response.metadata.quality_status ?? "N/A"}
              </p>

              <p>
                Evidence:{" "}
                {response.evidence_references.length > 0
                  ? response.evidence_references.join(", ")
                  : "Package-level evidence"}
              </p>
            </div>
          </div>

          {response.limitation && (
            <div className="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-4">
              <h3 className="text-sm font-semibold text-amber-900">
                Limitation
              </h3>

              <p className="mt-1 text-xs leading-5 text-amber-900">
                {response.limitation}
              </p>
            </div>
          )}

          {response.suggested_follow_ups &&
            response.suggested_follow_ups.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-semibold text-gray-500">
                  Suggested questions
                </p>

                <div className="mt-2 flex flex-wrap gap-2">
                  {response.suggested_follow_ups.map(
                    (followUp) => (
                      <button
                        key={followUp}
                        type="button"
                        onClick={() =>
                          setQuestion(followUp)
                        }
                        className="rounded-full border bg-white px-3 py-2 text-xs hover:bg-gray-50"
                      >
                        {followUp}
                      </button>
                    )
                  )}
                </div>
              </div>
            )}
        </div>
      )}
    </section>
  );
}