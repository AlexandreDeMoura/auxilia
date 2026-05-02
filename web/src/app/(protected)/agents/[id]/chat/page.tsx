"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { v4 as uuidv4 } from "uuid";
import {
	type PromptInputMessage,
	usePromptInputController,
} from "@/components/ai-elements/prompt-input";
import ChatPromptInput from "./components/prompt-input";
import { SelectAgentDialog } from "./components/select-agent-dialog";
import { useThreadsStore } from "@/stores/threads-store";
import { usePendingMessageStore } from "@/stores/pending-message-store";
import { useModelsStore } from "@/stores/models-store";
import { useUserStore } from "@/stores/user-store";
import { api } from "@/lib/api/client";
import { ChevronDown } from "lucide-react";
import { Agent } from "@/types/agents";
import { ThinkingEffort } from "@/types/threads";
import { AgentAvatar } from "@/components/ui/agent-avatar";
import { SageAlert } from "@/components/ui/sage-alert";
import { getDefaultModel } from "@/lib/utils/get-default-model";
import { useAgentReadiness } from "@/hooks/use-agent-readiness";

const StarterChatPage = () => {
	const params = useParams();
	const router = useRouter();
	const agentId = params.id as string;
	const [isCreating, setIsCreating] = useState(false);
	const { modelSelection, starterAgent } = usePromptInputController();
	const selectedModel = modelSelection.value;
	const setSelectedModel = modelSelection.setModel;
	const setStarterAgent = starterAgent.set;
	const addThread = useThreadsStore((state) => state.addThread);
	const setPendingMessage = usePendingMessageStore(
		(state) => state.setPendingMessage,
	);
	const models = useModelsStore((state) => state.models);
	const fetchModels = useModelsStore((state) => state.fetchModels);
	const user = useUserStore((state) => state.user);
	const fetchUser = useUserStore((state) => state.fetchUser);
	const [agent, setAgent] = useState<Agent | null>(null);
	const [isAgentDialogOpen, setIsAgentDialogOpen] = useState(false);
	const [thinkingEnabled, setThinkingEnabled] = useState(true);
	const [thinkingEffort, setThinkingEffort] = useState<ThinkingEffort>("medium");
	const {
		ready: agentReady,
		status,
		disconnectedMcpServers,
		refetch: refetchReady,
	} = useAgentReadiness(agentId);
	const thinkingControlsEnabled = user?.thinkingControlsEnabled ?? false;

	const handleSubmit = async (message: PromptInputMessage) => {
		if (!message) return;

		const hasText = "text" in message && message.text?.trim();
		const hasFiles =
			"files" in message && message.files && message.files.length > 0;

		if (!hasText && !hasFiles) {
			return;
		}

		const modelId = selectedModel ?? getDefaultModel(models);
		if (!modelId) {
			console.error("No model available to create thread");
			return;
		}
		const modelEntry = models.find((m) => m.id === modelId);

		setIsCreating(true);

		try {
			// Generate thread ID on frontend
			const threadId = uuidv4();

			// Store the pending message (with files) to be consumed by the thread page
			setPendingMessage(threadId, message);

			// Extract text for display purposes (thread list preview)
			const textContent = "text" in message ? message.text : undefined;
			const threadPayload: {
				id: string;
				agentId: string;
				modelId: string;
				firstMessageContent: string | undefined;
				thinkingEnabled?: boolean;
				thinkingEffort?: ThinkingEffort;
			} = {
				id: threadId,
				agentId: agentId,
				modelId,
				firstMessageContent: textContent,
			};

			if (thinkingControlsEnabled && modelEntry?.supportsThinking) {
				threadPayload.thinkingEnabled = thinkingEnabled;
				if (modelEntry.supportsThinkingEffort && thinkingEnabled) {
					threadPayload.thinkingEffort = thinkingEffort;
				}
			}

			const response = await api.post("/threads", threadPayload);

			const thread = {
				...response.data,
				agentName: agent?.name ?? null,
				agentEmoji: agent?.emoji ?? null,
				agentColor: agent?.color ?? null,
			};

			addThread(thread);

			router.push(`/agents/${agentId}/chat/${threadId}`);
		} catch (error) {
			console.error("Error creating thread:", error);
			setIsCreating(false);
		}
	};

	useEffect(() => {
		if (models.length === 0) {
			fetchModels().catch((error) => {
				console.error("Error fetching models:", error);
			});
		}
	}, [fetchModels, models.length]);

	useEffect(() => {
		fetchUser().catch((error) => {
			console.error("Error fetching user settings:", error);
		});
	}, [fetchUser]);

	useEffect(() => {
		if (selectedModel) {
			return;
		}

		const defaultModel = getDefaultModel(models);
		if (defaultModel) {
			setSelectedModel(defaultModel);
		}
	}, [models, selectedModel, setSelectedModel]);

	useEffect(() => {
		const fetchAgent = async () => {
			const response = await api.get(`/agents/${agentId}`);
			const agent = response.data;
			setAgent(agent);
			setStarterAgent({ name: agent.name, emoji: agent.emoji });
		};
		fetchAgent();
	}, [agentId, setStarterAgent]);

	return (
		<div className="container mx-auto h-full flex flex-col items-center justify-center max-w-4xl px-6">
			<div className="w-full max-w-3xl space-y-8">
				<div className="text-center space-y-4">
					<button
						onClick={() => setIsAgentDialogOpen(true)}
						className="flex items-center justify-center gap-2 mx-auto hover:opacity-80 transition-opacity cursor-pointer"
					>
						<AgentAvatar
							color={agent?.color}
							emoji={agent?.emoji || starterAgent.value?.emoji}
							size="lg"
						/>
						<h1 className="text-4xl font-bold">
							{agent?.name || starterAgent.value?.name}
						</h1>
						<ChevronDown className="size-5 text-muted-foreground ml-8 mt-1" />
					</button>
					{status !== "not_configured" && (
						<p className="text-lg text-muted-foreground">
							Ask me anything to begin
						</p>
					)}
				</div>

				<div className="w-full">
					{status === "not_configured" ? (
						<SageAlert
							variant="error"
							message="Agent is not configured yet. Contact agent owner to configure it first."
							dismissible={false}
						/>
					) : (
						<ChatPromptInput
							onSubmit={handleSubmit}
							status={isCreating ? "streaming" : "ready"}
							className="w-full"
							selectedModel={selectedModel}
							onModelChange={setSelectedModel}
							thinkingControlsEnabled={thinkingControlsEnabled}
							thinkingEnabled={thinkingEnabled}
							onThinkingEnabledChange={setThinkingEnabled}
							thinkingEffort={thinkingEffort}
							onThinkingEffortChange={setThinkingEffort}
							agentReady={agentReady}
							disconnectedServers={disconnectedMcpServers}
							onAllConnected={refetchReady}
						/>
					)}
				</div>

				<SelectAgentDialog
					open={isAgentDialogOpen}
					onOpenChange={setIsAgentDialogOpen}
					onAgentSelect={(a) =>
						starterAgent.set({ name: a.name, emoji: a.emoji ?? null })
					}
				/>
			</div>
		</div>
	);
};

export default StarterChatPage;
