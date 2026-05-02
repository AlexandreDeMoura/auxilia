export interface Model {
	id: string;
	name: string;
	chef: string;
	chefSlug: string;
	providers: string[];
	supportsThinking: boolean;
	supportsThinkingEffort: boolean;
}
