import { create } from "zustand";
import { api } from "@/lib/api/client";
import { Model } from "@/types/models";

interface ModelsState {
	models: Model[];
	isInitialized: boolean;
	fetchModels: () => Promise<void>;
}

export const useModelsStore = create<ModelsState>((set, get) => ({
	models: [],
	isInitialized: false,
	fetchModels: async () => {
		if (get().isInitialized) {
			return;
		}

		try {
			const response = await api.get("/model-providers/models");
			set({ models: response.data, isInitialized: true });
		} catch (error) {
			console.error("Error fetching models:", error);
			set({ isInitialized: true });
			throw error;
		}
	},
}));
