"use client";

import { useState } from "react";

type Evidence = {
  result_id?: string;
  data_version?: string;
  method_version?: string;
  quality_status?: string;
  [key: string]: unknown;
};

type AssistantResponse = {
  answer?: string;
  answer_mode?: string;
  intent?: string;
  status?: string;
  code?: string;
  message?: string;
  evidence?: Evidence | Evidence[];
  result_id?: string;
  data_version?: string;
  method_version?: string;
  quality_status?: string;
};

export default function GroundedAssistant() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] =
    useState<AssistantResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askAssistant() {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const apiBaseUrl =
        process.env.NEXT_PUBLIC_API_BASE_URL;

      if (!apiBaseUrl) {
        throw new Error(
          "NEXT_PUBLIC_API_BASE_URL is not configured."
        );
      }

      const response = await fetch(
        `${apiBaseUrl}/api/assistant`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: trimmedQuestion,
          }),
        }
      );

      const data =
        (await response.json()) as AssistantResponse;

      if (!response.ok) {
        if (data.code === "MISSING_PARAMETER") {
          setResponse(data);
          return;
        }

        throw new Error(
          data.message ||
            data.answer ||
            "Assistant request failed."
        );
      }

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
    <section className="rounded-xl border bg-white p-5 shadow-sm">
      <div>
        <h2 className="text-lg font-semibold">
          Grounded Assistant
        </h2>

        <p className="mt-1 text-sm text-gray-600">
          Ask questions about the approved intelligence
          evidence. Responses are grounded in the scoped
          analytical results.
        </p>
      </div>

      <div className="mt-4 flex flex-col gap-3">
        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask a question about the intelligence results..."
          rows={3}
          className="w-full rounded-lg border px-3 py-2 text-sm outline-none focus:ring-2"
          disabled={loading}
        />

        <div>
          <button
            type="button"
            onClick={askAssistant}
            disabled={loading || !question.trim()}
            className="rounded-lg border bg-black px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Asking..." : "Ask Assistant"}
          </button>
        </div>
      </div>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">
            {error}
          </p>
        </div>
      )}

      {response && (
        <div className="mt-5 space-y-4">

          {response.code === "MISSING_PARAMETER" && (
            <div className="rounded-lg border border-amber-300 bg-amber-50 p-4">
              <p className="text-sm font-semibold text-amber-900">
                Missing parameter
              </p>

              <p className="mt-1 text-sm text-amber-800">
                {response.message ||
                  response.answer ||
                  "Additional information is required."}
              </p>
            </div>
          )}

          {response.answer && (
            <div className="rounded-lg border bg-gray-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                Answer
              </p>

              <p className="mt-2 whitespace-pre-wrap text-sm text-gray-800">
                {response.answer}
              </p>
            </div>
          )}

          {response.answer_mode && (
            <div className="rounded-lg border bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                Answer Mode
              </p>

              <p className="mt-1 font-mono text-sm font-semibold">
                {response.answer_mode}
              </p>
            </div>
          )}

          {response.intent && (
            <div className="rounded-lg border bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                Intent
              </p>

              <p className="mt-1 font-mono text-sm">
                {response.intent}
              </p>
            </div>
          )}

          {(response.result_id ||
            response.data_version ||
            response.method_version ||
            response.quality_status) && (
            <div className="rounded-lg border bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                Evidence
              </p>

              <div className="mt-2 space-y-1 text-sm">
                {response.result_id && (
                  <p>
                    <strong>Result ID:</strong>{" "}
                    {response.result_id}
                  </p>
                )}

                {response.data_version && (
                  <p>
                    <strong>Data version:</strong>{" "}
                    {response.data_version}
                  </p>
                )}

                {response.method_version && (
                  <p>
                    <strong>Method version:</strong>{" "}
                    {response.method_version}
                  </p>
                )}

                {response.quality_status && (
                  <p>
                    <strong>Quality:</strong>{" "}
                    {response.quality_status}
                  </p>
                )}
              </div>
            </div>
          )}

          {response.evidence && (
            <details className="rounded-lg border bg-gray-50 p-4">
              <summary className="cursor-pointer text-sm font-semibold">
                Evidence details
              </summary>

              <pre className="mt-3 overflow-x-auto whitespace-pre-wrap text-xs">
                {JSON.stringify(
                  response.evidence,
                  null,
                  2
                )}
              </pre>
            </details>
          )}

        </div>
      )}
    </section>
  );
}