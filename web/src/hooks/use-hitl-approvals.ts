import { useCallback, useEffect, useMemo, useRef, useState } from "react";

export type HitlDecision = "approve" | "reject";

/** How long a pending approval waits for the user before it is denied. */
export const HITL_AUTO_REJECT_MS = 5000;

/** The running auto-deny countdown: `key` changes each time it restarts. */
export type HitlAutoReject = { afterMs: number; key: string };

/**
 * The `input.respond` payload. Addressed form (interrupt id + decisions keyed
 * by tool-call id): the backend validates the batch against the checkpoint (a
 * stale approval is a 409, not a resume of whatever pends now) and orders the
 * decisions itself. Positional form (`{type}` only, in action-request order):
 * used when a pending call has no id — the backend keys such calls
 * `approval-<index>`, which the client cannot reproduce.
 */
export type HitlResponse = {
	decisions: { tool_call_id?: string; type: HitlDecision }[];
};

type UseHitlApprovalsArgs<TPending extends { id: string }> = {
	/** Id of the pending interrupt; `null` forces the positional form. */
	interruptId: string | null;
	/** The tool calls the interrupt is waiting on; empty when not interrupted. */
	pendingToolCalls: TPending[];
	/** Resume the run — `stream.respond(response, { interruptId })`. */
	respond: (response: HitlResponse, interruptId: string | null) => void;
	/** Hold a complete batch until this is true (e.g. another resume is in
	 *  flight — the thread accepts one run at a time). Default: send at once. */
	enabled?: boolean;
	/** Deny the calls still undecided after this long without a decision from
	 *  the user; `null` waits forever (e.g. the approval cannot be answered). */
	autoRejectAfterMs?: number | null;
};

/**
 * Collects one approve/reject decision per pending tool call and, once the
 * batch is complete, resumes the interrupted run exactly once. Calls the user
 * leaves undecided are denied after `autoRejectAfterMs`; every decision the
 * user makes restarts that countdown for the calls still waiting.
 */
export function useHitlApprovals<TPending extends { id: string }>({
	interruptId,
	pendingToolCalls,
	respond,
	enabled = true,
	autoRejectAfterMs = HITL_AUTO_REJECT_MS,
}: UseHitlApprovalsArgs<TPending>) {
	const [decisions, setDecisions] = useState<Record<string, HitlDecision>>({});
	const submittedBatch = useRef<string | null>(null);

	useEffect(() => {
		if (!enabled || pendingToolCalls.length === 0) return;
		if (!pendingToolCalls.every((tc) => decisions[tc.id])) return;

		const batchKey =
			interruptId ?? pendingToolCalls.map((tc) => tc.id).join("|");
		if (submittedBatch.current === batchKey) return;
		submittedBatch.current = batchKey;

		respond(
			{
				decisions: pendingToolCalls.map((tc) =>
					interruptId
						? { tool_call_id: tc.id, type: decisions[tc.id] }
						: { type: decisions[tc.id] },
				),
			},
			interruptId,
		);
	}, [enabled, interruptId, pendingToolCalls, decisions, respond]);

	const undecidedKey = pendingToolCalls
		.filter((tc) => !decisions[tc.id])
		.map((tc) => tc.id)
		.join("|");
	const autoReject = useMemo<HitlAutoReject | null>(
		() =>
			autoRejectAfterMs == null || undecidedKey === ""
				? null
				: { afterMs: autoRejectAfterMs, key: undecidedKey },
		[autoRejectAfterMs, undecidedKey],
	);

	useEffect(() => {
		if (autoReject == null) return;
		const undecided = autoReject.key.split("|");
		const timer = setTimeout(() => {
			setDecisions((prev) => {
				const next = { ...prev };
				for (const id of undecided) next[id] ??= "reject";
				return next;
			});
		}, autoReject.afterMs);
		return () => {
			clearTimeout(timer);
		};
	}, [autoReject]);

	const recordDecision = useCallback(
		(toolCallId: string, type: HitlDecision) => {
			setDecisions((prev) => ({ ...prev, [toolCallId]: type }));
		},
		[],
	);

	return { decisions, recordDecision, autoReject };
}
