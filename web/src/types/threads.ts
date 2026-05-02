export const THINKING_EFFORT_LEVELS = ["low", "medium", "high"] as const;

export type ThinkingEffort = (typeof THINKING_EFFORT_LEVELS)[number];

export function isThinkingEffort(value: unknown): value is ThinkingEffort {
	return (
		typeof value === "string" &&
		THINKING_EFFORT_LEVELS.includes(value as ThinkingEffort)
	);
}

export interface Thread {
	id: string;
	agentId: string;
	modelId?: string | null;
	thinkingEnabled?: boolean | null;
	thinkingEffort?: ThinkingEffort | null;
	firstMessageContent: string;
	agentName: string | null;
	agentEmoji: string | null;
	agentColor: string | null;
	agentArchived: boolean;
	createdAt: string;
}
