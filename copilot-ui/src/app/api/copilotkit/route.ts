import {
  CopilotRuntime,
  ExperimentalOllamaAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

export const POST = async (req: NextRequest) => {
  const runtime = new CopilotRuntime();

  // L'adaptateur Ollama est passé dans les options de l'endpoint
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter: new ExperimentalOllamaAdapter({
      model: "mistral", // Modèle gratuit, téléchargeable avec : ollama pull mistral
    }),
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
