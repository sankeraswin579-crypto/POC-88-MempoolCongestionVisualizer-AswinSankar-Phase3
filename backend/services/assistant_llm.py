
from __future__ import annotations

import json
import os
from typing import Any

import requests


GROUNDING_SYSTEM_PROMPT = """
You are the explanation layer of a bounded data assistant.

Your job is ONLY to explain the supplied approved evidence.

RULES:
1. Answer only from the supplied evidence.
2. Never access the canonical dataset.
3. Never calculate or derive new values.
4. Never estimate, predict, forecast, rank, or invent findings.
5. Never invent evidence IDs.
6. Preserve the supplied limitation.
7. Use only supplied numbers and facts.
8. If evidence is insufficient, clearly say it cannot be answered from
   the approved evidence.
9. Keep the answer concise and factual.
10. Return JSON only.

Required JSON:
{
  "answer": "answer based only on evidence",
  "evidence_references": ["existing evidence IDs only"]
}
""".strip()


class LLMService:
    """
    Bounded Gemini/OpenAI explanation service.

    The LLM receives only the user's scoped question, intent,
    and approved evidence package.
    """

    def __init__(self) -> None:
        self.provider = os.getenv(
            "ASSISTANT_LLM_PROVIDER",
            "gemini",
        ).strip().lower()

        self.api_key = (
            os.getenv("ASSISTANT_LLM_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or ""
        ).strip()

        self.model = os.getenv(
            "ASSISTANT_LLM_MODEL",
            "gemini-2.5-flash",
        ).strip()

        try:
            self.timeout = int(
                os.getenv(
                    "ASSISTANT_LLM_TIMEOUT",
                    "30",
                )
            )
        except ValueError:
            self.timeout = 30

    @property
    def available(self) -> bool:
        return bool(
            self.provider != "disabled"
            and self.api_key
            and self.model
        )

    def explain(
        self,
        question: str,
        intent_name: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any] | None:

        if not self.available:
            print(
                "[ASSISTANT_LLM] "
                "LLM unavailable. "
                f"provider={self.provider}, "
                f"model={self.model}, "
                f"key_set={bool(self.api_key)}"
            )
            return None

        package = self._build_package(
            question,
            intent_name,
            evidence,
        )

        try:
            if self.provider == "gemini":
                return self._gemini(package)

            if self.provider == "openai":
                return self._openai(package)

            print(
                "[ASSISTANT_LLM_ERROR] "
                f"Unsupported provider: {self.provider}"
            )
            return None

        except requests.RequestException as exc:
            print(
                "[ASSISTANT_LLM_ERROR] "
                f"{type(exc).__name__}: {exc}"
            )
            return None

        except Exception as exc:
            print(
                "[ASSISTANT_LLM_ERROR] "
                f"{type(exc).__name__}: {exc}"
            )
            return None

    # ============================================================
    # BUILD BOUNDED PACKAGE
    # ============================================================

    def _build_package(
        self,
        question: str,
        intent_name: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:

        metadata = evidence.get(
            "package_metadata",
            {},
        )

        package = {
            "question": question,
            "intent": intent_name,
            "evidence_type": evidence.get("type"),
            "evidence_references": evidence.get(
                "evidence_references",
                [],
            ),
            "data_version": metadata.get(
                "data_version"
            ),
            "method_version": metadata.get(
                "method_version"
            ),
            "quality_status": metadata.get(
                "quality_status"
            ),
            "limitation": metadata.get(
                "limitation"
            ),
        }

        evidence_type = evidence.get("type")

        # --------------------------------------------------------
        # SUMMARY
        # --------------------------------------------------------

        if evidence_type == "summary":
            summary = evidence.get(
                "summary",
                {},
            )

            package["values"] = {
                "record_count": summary.get(
                    "record_count"
                ),
                "comparative_group_count": summary.get(
                    "comparative_group_count"
                ),
                "finding_count": summary.get(
                    "finding_count"
                ),
                "interpretation": summary.get(
                    "interpretation"
                ),
                "data_version": summary.get(
                    "data_version"
                ),
                "validation_status": summary.get(
                    "validation_status"
                ),
                "temporal_context": summary.get(
                    "temporal_context"
                ),
            }

            return package

        # --------------------------------------------------------
        # COMPARISON GROUPS
        # --------------------------------------------------------

        if evidence_type == "comparison_groups":
            groups = evidence.get(
                "groups",
                [],
            )

            package["values"] = {
                "groups": [
                    {
                        "result_id": item.get(
                            "result_id"
                        ),
                        "metric_name": item.get(
                            "metric_name"
                        ),
                        "category": item.get(
                            "category"
                        ),
                        "result_value": item.get(
                            "result_value"
                        ),
                        "result_unit": item.get(
                            "result_unit",
                            item.get("unit"),
                        ),
                        "method_version": item.get(
                            "method_version"
                        ),
                        "data_version": item.get(
                            "data_version"
                        ),
                        "quality_status": item.get(
                            "quality_status"
                        ),
                    }
                    for item in groups
                ]
            }

            return package

        # --------------------------------------------------------
        # FRESHNESS
        # --------------------------------------------------------

        if evidence_type == "freshness":
            package["values"] = {
                "data_version": evidence.get(
                    "data_version"
                ),
                "method_versions": evidence.get(
                    "method_versions",
                    [],
                ),
                "generated_at": evidence.get(
                    "generated_at"
                ),
                "validation_status": evidence.get(
                    "validation_status"
                ),
            }

            return package

        # --------------------------------------------------------
        # CONGESTION SCORE
        # --------------------------------------------------------

        if evidence_type == "congestion_score":
            package["values"] = {
                "score": evidence.get(
                    "score",
                    evidence.get("value"),
                ),
                "label": evidence.get(
                    "label"
                ),
                "metric_name": evidence.get(
                    "metric_name"
                ),
                "result_unit": evidence.get(
                    "result_unit"
                ),
                "interpretation": evidence.get(
                    "interpretation"
                ),
            }

            return package

        # --------------------------------------------------------
        # RESULT EVIDENCE
        # --------------------------------------------------------

        item = evidence.get(
            "item",
            {},
        )

        item_evidence = item.get(
            "evidence",
            {},
        )

        package["result"] = {
            "result_id": item.get(
                "result_id"
            ),
            "metric_name": item.get(
                "metric_name"
            ),
            "category": item.get(
                "category"
            ),
            "result_value": item.get(
                "result_value"
            ),
            "result_unit": item.get(
                "result_unit"
            ),
            "finding": item.get(
                "finding"
            ),
            "finding_type": item.get(
                "finding_type"
            ),
            "baseline_method": item.get(
                "baseline_method"
            ),
            "method_version": item.get(
                "method_version"
            ),
            "data_version": item.get(
                "data_version"
            ),
            "generated_at": item.get(
                "generated_at"
            ),
            "limitation": item.get(
                "limitation"
            ),
        }

        if evidence_type == "baseline":
            package["values"] = {
                "baseline": evidence.get(
                    "value",
                    item_evidence.get(
                        "baseline_value"
                    ),
                ),
                "observation_count": evidence.get(
                    "observation_count",
                    item_evidence.get(
                        "observation_count"
                    ),
                ),
            }

        elif evidence_type == "range":
            package["values"] = {
                "minimum": evidence.get(
                    "minimum",
                    item_evidence.get(
                        "minimum"
                    ),
                ),
                "maximum": evidence.get(
                    "maximum",
                    item_evidence.get(
                        "maximum"
                    ),
                ),
                "range": evidence.get(
                    "range",
                    item_evidence.get(
                        "range"
                    ),
                ),
                "observation_count": evidence.get(
                    "observation_count",
                    item_evidence.get(
                        "observation_count"
                    ),
                ),
            }

        elif evidence_type == "extreme":
            package["values"] = {
                "extreme": evidence.get(
                    "extreme"
                ),
                "value": evidence.get(
                    "value"
                ),
            }

        elif evidence_type == "comparison":
            package["values"] = {
                "observed_value": evidence.get(
                    "value",
                    evidence.get(
                        "observed_value"
                    ),
                ),
                "baseline": evidence.get(
                    "baseline"
                ),
                "difference": evidence.get(
                    "difference"
                ),
            }

        elif evidence_type == "result_explanation":
            package["values"] = {
                "observation_count": evidence.get(
                    "observation_count",
                    item_evidence.get(
                        "observation_count"
                    ),
                ),
                "baseline": evidence.get(
                    "baseline",
                    item_evidence.get(
                        "baseline_value"
                    ),
                ),
                "finding": evidence.get(
                    "finding",
                    item.get("finding"),
                ),
            }

        elif evidence_type == "method":
            package["values"] = {
                "track": evidence.get(
                    "track",
                    evidence.get(
                        "primary_track"
                    ),
                ),
                "baseline_method": evidence.get(
                    "baseline_method",
                    item.get(
                        "baseline_method"
                    ),
                ),
                "method_version": evidence.get(
                    "method_version",
                    item.get(
                        "method_version"
                    ),
                ),
            }

        elif evidence_type == "limitation":
            package["values"] = {
                "approved_track": evidence.get(
                    "approved_track",
                    evidence.get(
                        "primary_track"
                    ),
                ),
                "summary_limitation": evidence.get(
                    "summary_limitation"
                ),
            }

        else:
            package["values"] = {}

        return package

    # ============================================================
    # GEMINI
    # ============================================================

    def _gemini(
        self,
        package: dict[str, Any],
    ) -> dict[str, Any] | None:

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/"
            f"{self.model}:generateContent"
        )

        payload = {
            "system_instruction": {
                "parts": [
                    {
                        "text": GROUNDING_SYSTEM_PROMPT,
                    }
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": json.dumps(
                                package,
                                ensure_ascii=False,
                            )
                        }
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json",
            },
        }

        response = requests.post(
            url,
            params={
                "key": self.api_key,
            },
            json=payload,
            timeout=self.timeout,
        )

        if response.status_code >= 400:
            print(
                "[GEMINI ERROR] "
                f"HTTP {response.status_code}"
            )
            print(
                response.text[:1500]
            )

        response.raise_for_status()

        data = response.json()

        candidates = data.get(
            "candidates",
            [],
        )

        if not candidates:
            print(
                "[GEMINI ERROR] "
                "No candidates returned."
            )
            return None

        candidate = candidates[0]

        parts = (
            candidate
            .get("content", {})
            .get("parts", [])
        )

        if not parts:
            print(
                "[GEMINI ERROR] "
                "No response parts."
            )
            return None

        content = parts[0].get(
            "text"
        )

        if not content:
            print(
                "[GEMINI ERROR] "
                "No response text."
            )
            return None

        parsed = self._parse_json(
            content
        )

        if parsed is None:
            print(
                "[GEMINI ERROR] "
                "Response was not valid JSON."
            )
            print(
                content[:1000]
            )
            return None

        return self._validate_response(
            parsed,
            package,
        )

    # ============================================================
    # OPENAI
    # ============================================================

    def _openai(
        self,
        package: dict[str, Any],
    ) -> dict[str, Any] | None:

        url = (
            "https://api.openai.com/v1/chat/completions"
        )

        headers = {
            "Authorization": (
                f"Bearer {self.api_key}"
            ),
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "temperature": 0,
            "response_format": {
                "type": "json_object",
            },
            "messages": [
                {
                    "role": "system",
                    "content": GROUNDING_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        package,
                        ensure_ascii=False,
                    ),
                },
            ],
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )

        if response.status_code >= 400:
            print(
                "[OPENAI ERROR] "
                f"HTTP {response.status_code}"
            )
            print(
                response.text[:1500]
            )

        response.raise_for_status()

        data = response.json()

        choices = data.get(
            "choices",
            [],
        )

        if not choices:
            print(
                "[OPENAI ERROR] "
                "No choices returned."
            )
            return None

        content = (
            choices[0]
            .get("message", {})
            .get("content")
        )

        if not content:
            print(
                "[OPENAI ERROR] "
                "No response content."
            )
            return None

        parsed = self._parse_json(
            content
        )

        if parsed is None:
            print(
                "[OPENAI ERROR] "
                "Response was not valid JSON."
            )
            return None

        return self._validate_response(
            parsed,
            package,
        )

    # ============================================================
    # VALIDATION
    # ============================================================

    @staticmethod
    def _validate_response(
        parsed: dict[str, Any],
        package: dict[str, Any],
    ) -> dict[str, Any] | None:

        answer = parsed.get(
            "answer"
        )

        references = parsed.get(
            "evidence_references",
            [],
        )

        if not isinstance(
            answer,
            str,
        ):
            print(
                "[LLM ERROR] "
                "Missing answer."
            )
            return None

        if not isinstance(
            references,
            list,
        ):
            print(
                "[LLM ERROR] "
                "Invalid evidence_references."
            )
            return None

        allowed = set(
            package.get(
                "evidence_references",
                [],
            )
        )

        invalid = [
            ref
            for ref in references
            if ref not in allowed
        ]

        if invalid:
            print(
                "[LLM ERROR] "
                f"Invalid evidence references: {invalid}"
            )
            return None

        return {
            "answer": answer.strip(),
            "evidence_references": references,
        }

    # ============================================================
    # JSON HELPERS
    # ============================================================

    @staticmethod
    def _parse_json(
        content: str,
    ) -> dict[str, Any] | None:

        content = content.strip()

        if content.startswith("```"):
            lines = content.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(
                lines
            ).strip()

        try:
            result = json.loads(
                content
            )
        except json.JSONDecodeError:
            return None

        if not isinstance(
            result,
            dict,
        ):
            return None

        return result


