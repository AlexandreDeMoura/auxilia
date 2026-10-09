import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { HITL_AUTO_REJECT_MS, useHitlApprovals } from "./use-hitl-approvals";

const calls = (...ids: string[]) => ids.map((id) => ({ id }));

describe("useHitlApprovals auto-deny", () => {
	beforeEach(() => {
		vi.useFakeTimers();
	});
	afterEach(() => {
		vi.useRealTimers();
	});

	it("denies every undecided call once the delay passes without a decision", () => {
		const respond = vi.fn();
		const pendingToolCalls = calls("a", "b");
		renderHook(() =>
			useHitlApprovals({ interruptId: "i1", pendingToolCalls, respond }),
		);

		act(() => {
			vi.advanceTimersByTime(HITL_AUTO_REJECT_MS - 1);
		});
		expect(respond).not.toHaveBeenCalled();

		act(() => {
			vi.advanceTimersByTime(1);
		});
		expect(respond).toHaveBeenCalledExactlyOnceWith(
			{
				decisions: [
					{ tool_call_id: "a", type: "reject" },
					{ tool_call_id: "b", type: "reject" },
				],
			},
			"i1",
		);
	});

	it("restarts the countdown on a decision and keeps the user's answer", () => {
		const respond = vi.fn();
		const pendingToolCalls = calls("a", "b");
		const { result } = renderHook(() =>
			useHitlApprovals({ interruptId: "i1", pendingToolCalls, respond }),
		);

		act(() => {
			vi.advanceTimersByTime(HITL_AUTO_REJECT_MS - 1000);
		});
		act(() => {
			result.current.recordDecision("a", "approve");
		});
		act(() => {
			vi.advanceTimersByTime(HITL_AUTO_REJECT_MS - 1);
		});
		expect(respond).not.toHaveBeenCalled();

		act(() => {
			vi.advanceTimersByTime(1);
		});
		expect(respond).toHaveBeenCalledExactlyOnceWith(
			{
				decisions: [
					{ tool_call_id: "a", type: "approve" },
					{ tool_call_id: "b", type: "reject" },
				],
			},
			"i1",
		);
	});

	it("does not fire once the user has answered everything", () => {
		const respond = vi.fn();
		const pendingToolCalls = calls("a");
		const { result } = renderHook(() =>
			useHitlApprovals({ interruptId: "i1", pendingToolCalls, respond }),
		);

		act(() => {
			result.current.recordDecision("a", "approve");
		});
		expect(result.current.autoReject).toBeNull();
		act(() => {
			vi.advanceTimersByTime(HITL_AUTO_REJECT_MS * 2);
		});
		expect(respond).toHaveBeenCalledTimes(1);
		expect(result.current.decisions).toEqual({ a: "approve" });
	});

	it("waits forever when the delay is null", () => {
		const respond = vi.fn();
		const pendingToolCalls = calls("a");
		const { result } = renderHook(() =>
			useHitlApprovals({
				interruptId: "i1",
				pendingToolCalls,
				respond,
				autoRejectAfterMs: null,
			}),
		);

		act(() => {
			vi.advanceTimersByTime(HITL_AUTO_REJECT_MS * 2);
		});
		expect(result.current.autoReject).toBeNull();
		expect(respond).not.toHaveBeenCalled();
	});
});
