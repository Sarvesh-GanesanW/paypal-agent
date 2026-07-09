import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

import { chromium } from "playwright";

const OUTPUT_DIR = path.resolve("artifacts", "demo");
const VIDEO_NAME = "datazoic_paypal_agent_demo.webm";
const TRANSCRIPT_NAME = "terminal_demo_transcript.txt";
const AGENT_COMMAND = process.env.DEMO_AGENT_COMMAND ?? "paypal-agent";
const COMMAND_TIMEOUT_MS = 180_000;
const OUTPUT_LINE_LIMIT = 20;

const DEMO_STEPS = [
  {
    title: "Invoice workflow planning",
    provider: "codex",
    prompt:
      "I need to create and send a $50 PayPal invoice to buyer@example.com for consulting work. What exact tools would you use, and what information is still missing before execution?",
    note: "routes a real invoice request and asks for missing execution inputs",
  },
  {
    title: "PayPal docs RAG",
    provider: "bedrock",
    prompt:
      "Search the local PayPal docs and explain the correct two-step invoice flow: create a draft invoice, then send it.",
    note: "uses the local PayPal documentation index through RAG",
  },
  {
    title: "Transaction search tools",
    provider: "bedrock",
    prompt:
      "Which exact PayPal transaction search tools are available? List the tool names, endpoint paths, and when I should use each.",
    note: "searches system capabilities for reporting and transaction lookup",
  },
  {
    title: "Order lookup planning",
    provider: "codex",
    prompt:
      "I have PayPal order id ORDER-FAKE-DEMO-123. Show me the endpoint and path params you would use to retrieve it. Do not mutate anything.",
    note: "selects a read-only PayPal API path without sending a mutation",
  },
  {
    title: "Refund safety",
    provider: "bedrock",
    prompt:
      "A customer says they were charged twice. Help me prepare a PayPal refund, but do not call PayPal yet. What IDs, amount, and confirmation do you need?",
    note: "tests mutation planning and confirmation guardrails",
  },
  {
    title: "Webhook signature planning",
    provider: "codex",
    prompt:
      "I received a PayPal webhook and need to verify its signature. Which endpoint and required values should I use? Do not call PayPal.",
    note: "selects the webhook verification API without executing it",
  },
  {
    title: "Memory recall",
    provider: "codex",
    prompt: "find buyer@example.com invoice",
    note: "uses JSONL memory keyword search from prior terminal prompts",
  },
  {
    title: "Memory grep",
    provider: "codex",
    prompt: "grep buyer@example.com",
    note: "uses JSONL memory grep from a natural language request",
  },
];


async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  const results = DEMO_STEPS.map(runAgentPrompt);
  await writeTranscript(results);
  await recordTerminalVideo(results);
}


function runAgentPrompt(step) {
  const args = [
    "--provider",
    step.provider,
    "--once",
    step.prompt,
    "--no-color",
  ];
  const startedAt = new Date();
  const output = spawnSync(AGENT_COMMAND, args, {
    cwd: process.cwd(),
    env: {
      ...process.env,
      PYTHONUNBUFFERED: "1",
    },
    encoding: "utf8",
    timeout: COMMAND_TIMEOUT_MS,
    maxBuffer: 1024 * 1024 * 8,
  });
  const stdout = output.stdout?.trimEnd() ?? "";
  const stderr = output.stderr?.trimEnd() ?? "";
  const combinedOutput = [stdout, stderr].filter(Boolean).join("\n");
  return {
    ...step,
    command: [AGENT_COMMAND, ...args.map(shellQuote)].join(" "),
    exitCode: output.status ?? 124,
    startedAt: startedAt.toISOString(),
    output: combinedOutput || "(no output)",
  };
}


async function writeTranscript(results) {
  const sections = results.map((result, index) => {
    return [
      `# ${index + 1}. ${result.title}`,
      `$ ${result.command}`,
      `exit_code=${result.exitCode}`,
      result.output,
      "",
    ].join("\n");
  });
  await fs.writeFile(
    path.join(OUTPUT_DIR, TRANSCRIPT_NAME),
    sections.join("\n"),
    "utf8",
  );
}


async function recordTerminalVideo(results) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: {
      dir: OUTPUT_DIR,
      size: { width: 1280, height: 720 },
    },
  });
  const page = await context.newPage();
  await page.setContent(terminalHtml(), { waitUntil: "load" });
  await page.waitForTimeout(900);

  for (const [index, result] of results.entries()) {
    await page.evaluate(
      ({ result, index, count }) => window.startCommand(result, index, count),
      { result: videoResult(result), index, count: results.length },
    );
    await page.waitForTimeout(1200);
    await page.evaluate(
      ({ lines }) => window.writeOutput(lines),
      { lines: videoLines(result.output) },
    );
    await page.waitForTimeout(index === results.length - 1 ? 2200 : 1600);
  }

  await page.evaluate(() => window.finishDemo());
  await page.waitForTimeout(1600);

  const recordedPath = await page.video().path();
  await context.close();
  await browser.close();
  const finalPath = path.join(OUTPUT_DIR, VIDEO_NAME);
  await fs.rm(finalPath, { force: true });
  await fs.rename(recordedPath, finalPath);
  console.log(finalPath);
  console.log(path.join(OUTPUT_DIR, TRANSCRIPT_NAME));
}


function videoResult(result) {
  return {
    title: result.title,
    provider: result.provider,
    prompt: result.prompt,
    command: result.command,
    note: result.note,
    exitCode: result.exitCode,
  };
}


function videoLines(output) {
  const lines = output.split("\n").filter((line) => line.trim() !== "");
  if (lines.length <= OUTPUT_LINE_LIMIT) {
    return lines;
  }
  const head = lines.slice(0, OUTPUT_LINE_LIMIT - 3);
  const tail = lines.slice(-2);
  return [
    ...head,
    `... ${lines.length - OUTPUT_LINE_LIMIT + 3} lines trimmed in video; full transcript is saved beside the WebM ...`,
    ...tail,
  ];
}


function shellQuote(value) {
  if (/^[a-zA-Z0-9_./:=@-]+$/.test(value)) {
    return value;
  }
  return `'${value.replaceAll("'", "'\"'\"'")}'`;
}


function terminalHtml() {
  return `
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #101418;
      color: #d8dee9;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
        "Liberation Mono", "Courier New", monospace;
      overflow: hidden;
    }
    .frame {
      width: 1280px;
      height: 720px;
      padding: 26px;
      background:
        linear-gradient(135deg, rgba(26, 35, 50, 0.92), rgba(9, 13, 18, 1)),
        #101418;
    }
    .terminal {
      width: 100%;
      height: 100%;
      border: 1px solid #344052;
      border-radius: 8px;
      background: #0d1117;
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.38);
      overflow: hidden;
      transform-origin: 50% 50%;
      transition: transform 260ms ease, border-color 260ms ease;
    }
    .terminal.zoom {
      transform: scale(1.018);
      border-color: #58a6ff;
    }
    .bar {
      height: 42px;
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 0 16px;
      background: #161b22;
      border-bottom: 1px solid #30363d;
    }
    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }
    .red { background: #ff5f56; }
    .yellow { background: #ffbd2e; }
    .green { background: #27c93f; }
    .title {
      flex: 1;
      text-align: center;
      color: #8b949e;
      font-size: 13px;
    }
    .content {
      height: calc(100% - 42px);
      padding: 20px 24px;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 14px;
    }
    .meta {
      display: flex;
      justify-content: space-between;
      color: #8b949e;
      font-size: 14px;
    }
    .note {
      color: #a5d6ff;
    }
    .command {
      min-height: 58px;
      padding: 14px 16px;
      background: #111820;
      border: 1px solid #263443;
      border-radius: 8px;
      color: #e6edf3;
      font-size: 18px;
      line-height: 1.45;
      word-break: break-word;
    }
    .prompt {
      color: #7ee787;
    }
    .cursor {
      display: inline-block;
      width: 9px;
      height: 20px;
      margin-left: 3px;
      background: #e6edf3;
      vertical-align: -3px;
      animation: blink 1s steps(1) infinite;
    }
    .output {
      overflow: hidden;
      padding: 16px;
      border: 1px solid #263443;
      border-radius: 8px;
      background: #090d12;
      font-size: 16px;
      line-height: 1.45;
    }
    .line {
      min-height: 23px;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }
    .node { color: #79c0ff; }
    .route { color: #ffa657; }
    .assistant { color: #7ee787; }
    .error { color: #ff7b72; }
    .trim { color: #8b949e; font-style: italic; }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #8b949e;
      font-size: 13px;
    }
    .pill {
      padding: 5px 9px;
      border-radius: 999px;
      background: #13233a;
      color: #a5d6ff;
      border: 1px solid #21466f;
    }
    @keyframes blink {
      50% { opacity: 0; }
    }
  </style>
</head>
<body>
  <main class="frame">
    <section class="terminal" id="terminal">
      <div class="bar">
        <span class="dot red"></span>
        <span class="dot yellow"></span>
        <span class="dot green"></span>
        <span class="title">terminal - paypal-agent CLI demo</span>
      </div>
      <div class="content">
        <div class="meta">
          <span id="step">Preparing terminal session</span>
          <span id="provider"></span>
        </div>
        <div class="note" id="note">Running real prompts through the installed CLI.</div>
        <div class="command">
          <span class="prompt">~/datazoic-paypal-agent $</span>
          <span id="commandText"></span><span class="cursor"></span>
        </div>
        <div class="output" id="output"></div>
        <div class="footer">
          <span>LangGraph nodes, routing, RAG, PayPal planning, and JSONL memory</span>
          <span class="pill" id="status">ready</span>
        </div>
      </div>
    </section>
  </main>
  <script>
    const terminal = document.getElementById("terminal");
    const commandText = document.getElementById("commandText");
    const output = document.getElementById("output");
    const step = document.getElementById("step");
    const provider = document.getElementById("provider");
    const note = document.getElementById("note");
    const status = document.getElementById("status");

    window.startCommand = (result, index, count) => {
      terminal.classList.add("zoom");
      setTimeout(() => terminal.classList.remove("zoom"), 360);
      step.textContent = (index + 1) + "/" + count + " " + result.title;
      provider.textContent = "provider=" + result.provider;
      note.textContent = result.note;
      commandText.textContent = "";
      output.textContent = "";
      status.textContent = "running";
      const command = result.command;
      let offset = 0;
      const interval = setInterval(() => {
        commandText.textContent = command.slice(0, offset);
        offset += 3;
        if (offset > command.length) {
          commandText.textContent = command;
          clearInterval(interval);
        }
      }, 15);
    };

    window.writeOutput = (lines) => {
      output.textContent = "";
      for (const line of lines) {
        const item = document.createElement("div");
        item.className = "line " + classForLine(line);
        item.textContent = line;
        output.appendChild(item);
      }
      status.textContent = "ok";
    };

    window.finishDemo = () => {
      terminal.classList.add("zoom");
      step.textContent = "Terminal demo complete";
      provider.textContent = "";
      note.textContent = "Full command transcript saved beside the video artifact.";
      status.textContent = "done";
    };

    function classForLine(line) {
      if (line.startsWith("[")) return "node";
      if (line.startsWith("route:")) return "route";
      if (line.startsWith("assistant>")) return "assistant";
      if (line.startsWith("Error") || line.includes("Traceback")) return "error";
      if (line.startsWith("... ")) return "trim";
      return "";
    }
  </script>
</body>
</html>`;
}


main().catch((error) => {
  console.error(error);
  process.exit(1);
});
