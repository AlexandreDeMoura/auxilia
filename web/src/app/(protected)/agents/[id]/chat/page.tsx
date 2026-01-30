"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { type PromptInputMessage } from "@/components/ai-elements/prompt-input";
import ChatPromptInput from "./components/prompt-input";
import { useThreadsStore } from "@/stores/threads-store";
import { api } from "@/lib/api/client";
import { Agent } from "@/types/agents";
import { NewThreadDialog } from "@/components/layout/app-sidebar/new-thread-dialog";

const StarterChatPage = () => {
	const params = useParams();
	const router = useRouter();
	const agentId = params.id as string;
	const [isCreating, setIsCreating] = useState(false);
	const [selectedModel, setSelectedModel] = useState<string>("deepseek-chat");
	const addThread = useThreadsStore((state) => state.addThread);
	const [agent, setAgent] = useState<Agent | null>(null);
	const [isAgentDialogOpen, setIsAgentDialogOpen] = useState(false);

	const handleSubmit = async (message: PromptInputMessage) => {
		if (!message || !("text" in message) || !message.text?.trim()) {
			return;
		}

		setIsCreating(true);

		try {
			const response = await api.post("/threads", {
				agentId: agentId,
				firstMessageContent: message.text,
				modelId: selectedModel,
			});

			const thread = {
				...response.data,
				agentName: agent?.name ?? null,
				agentEmoji: agent?.emoji ?? null,
			};

			addThread(thread);

			router.push(`/agents/${agentId}/chat/${thread.id}`);
		} catch (error) {
			console.error("Error creating thread:", error);
			setIsCreating(false);
		}
	};

	useEffect(() => {
		const fetchAgent = async () => {
			const response = await api.get(`/agents/${agentId}`);
			const agent = response.data;
			setAgent(agent);
		};
		fetchAgent();
	}, [agentId]);

	return (
		<div className="container mx-auto h-full flex flex-col items-center justify-center max-w-4xl px-6">
			<div className="w-full max-w-3xl space-y-8">
				<div className="text-center space-y-4">
					<button
						onClick={() => setIsAgentDialogOpen(true)}
						className="flex items-center justify-center gap-2 mx-auto hover:opacity-80 transition-opacity cursor-pointer"
					>
						<div className="shrink-0 w-12 h-12 rounded-2xl bg-gray-100 text-2xl flex items-center justify-center">
							{agent?.emoji || "🤖"}
						</div>
						<h1 className="text-4xl font-bold">{agent?.name}</h1>
					</button>
					<p className="text-lg text-muted-foreground">
						Ask me anything to begin
					</p>
				</div>

				<div className="w-full">
					<ChatPromptInput
						onSubmit={handleSubmit}
						status={isCreating ? "streaming" : "ready"}
						className="w-full"
						selectedModel={selectedModel}
						onModelChange={setSelectedModel}
					/>
				</div>
			</div>

			<NewThreadDialog
				open={isAgentDialogOpen}
				onOpenChange={setIsAgentDialogOpen}
			/>
		</div>
	);
};

export default StarterChatPage;
