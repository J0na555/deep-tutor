/**
 * Deep Tutor OpenCode plugin — inject assembled preamble into the system prompt.
 *
 * Contract (system-design §5, §15 Integration): orchestrator output becomes part
 * of what OpenCode sends to the model via experimental.chat.system.transform.
 *
 * Disable per session: DEEP_TUTOR_OPENCODE=0
 * Override repo path: DEEP_TUTOR_ROOT=/path/to/deep-tutor
 */

import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const REPO_MARKERS = ["orchestrator/assemble.py", "configs/default.json"];

/** @type {Map<string, string>} */
const lastUserMessage = new Map();

function isDeepTutorRoot(dir) {
  return REPO_MARKERS.every((marker) => existsSync(join(dir, marker)));
}

function resolveDeepTutorRoot(cwd) {
  if (process.env.DEEP_TUTOR_ROOT) {
    const explicit = resolve(process.env.DEEP_TUTOR_ROOT);
    return isDeepTutorRoot(explicit) ? explicit : null;
  }

  let dir = resolve(cwd);
  while (true) {
    if (isDeepTutorRoot(dir)) {
      return dir;
    }
    const sibling = join(dir, "deep-tutor");
    if (isDeepTutorRoot(sibling)) {
      return resolve(sibling);
    }
    const parent = dirname(dir);
    if (parent === dir) {
      break;
    }
    dir = parent;
  }
  return null;
}

function extractUserText(parts) {
  if (!Array.isArray(parts)) {
    return "";
  }
  return parts
    .filter((part) => part && part.type === "text" && typeof part.text === "string")
    .map((part) => part.text)
    .join("\n")
    .trim();
}

function injectSystemBlock(output, block) {
  if (!block) {
    return;
  }
  if (output.system.length > 0) {
    output.system[output.system.length - 1] += `\n\n${block}`;
  } else {
    output.system.push(block);
  }
}

async function fetchPreamble($, repoRoot, cwd, message) {
  const hook = join(repoRoot, "scripts", "opencode-hook");
  const env = {};
  if (message) {
    env.DEEP_TUTOR_MESSAGE = message;
  }
  const result = await $`python3 ${hook} --cwd ${cwd}`.env(env).quiet().nothrow();
  if (result.exitCode !== 0) {
    return null;
  }
  try {
    return JSON.parse(result.stdout.toString());
  } catch {
    return null;
  }
}

export const DeepTutorPlugin = async ({ $, directory }) => {
  return {
    "chat.message": async (input, output) => {
      const text = extractUserText(output.parts);
      if (text && input.sessionID) {
        lastUserMessage.set(input.sessionID, text);
      }
    },

    "experimental.chat.system.transform": async (input, output) => {
      if (process.env.DEEP_TUTOR_OPENCODE === "0") {
        return;
      }

      const repoRoot = resolveDeepTutorRoot(directory);
      if (!repoRoot) {
        return;
      }

      const message =
        input.sessionID && lastUserMessage.has(input.sessionID)
          ? lastUserMessage.get(input.sessionID)
          : undefined;

      const payload = await fetchPreamble($, repoRoot, directory, message);
      if (payload?.text) {
        injectSystemBlock(output, payload.text);
      }
    },
  };
};
