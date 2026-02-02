import { create } from "zustand";
import { type PromptInputMessage } from "@/components/ai-elements/prompt-input";

interface PendingMessageState {
	pendingMessages: Map<string, PromptInputMessage>;
	setPendingMessage: (threadId: string, message: PromptInputMessage) => void;
	consumePendingMessage: (threadId: string) => PromptInputMessage | null;
}

export const usePendingMessageStore = create<PendingMessageState>(
	(set, get) => ({
		pendingMessages: new Map(),
		setPendingMessage: (threadId, message) =>
			set((state) => {
				const newMap = new Map(state.pendingMessages);
				newMap.set(threadId, message);
				return { pendingMessages: newMap };
			}),
		consumePendingMessage: (threadId) => {
			const message = get().pendingMessages.get(threadId);
			if (message) {
				set((state) => {
					const newMap = new Map(state.pendingMessages);
					newMap.delete(threadId);
					return { pendingMessages: newMap };
				});
			}
			return message ?? null;
		},
	}),
);
