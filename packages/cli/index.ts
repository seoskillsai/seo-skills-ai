#!/usr/bin/env node
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const action = args[0];
const target = args[1];
const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, '..', '..');
const inRepo = fs.existsSync(path.join(repoRoot, 'AGENTS.md')) && fs.existsSync(path.join(repoRoot, 'skills'));

console.log(`[seoskillsai CLI] SEO Skills AI v1.1.1`);

if (!action || action === 'help' || action === '--help') {
  console.log(`
This CLI is the in-repo launcher. The npm package is not published.

Install:
  git clone https://github.com/seoskillsai/seo-skills-ai.git
  cd seo-skills-ai
  # Unix:  bash install.sh
  # Win:   powershell -ExecutionPolicy Bypass -File .\\install.ps1
  # Then open this folder as the agent workspace.

Commands (from the cloned repo):
  node packages/cli/index.ts doctor
  python scripts/full_audit.py <url>
  python scripts/remediation_engine.py <url>
`);
  process.exit(0);
}

if (action === 'add') {
  if (!inRepo) {
    console.error('Clone https://github.com/seoskillsai/seo-skills-ai and open that folder as your workspace.');
    console.error('There is nothing to copy: skills load from the repository root.');
    process.exit(1);
  }
  console.log(`Workspace already contains SEO Skills (detected AGENTS.md + skills/).`);
  console.log(`Open this folder as the ${target || 'agent'} workspace. No extra install step is required.`);
  process.exit(0);
}

function runPython(scriptName, scriptArgs = []) {
  const scriptPath = path.join(repoRoot, 'scripts', scriptName);
  const py = spawn('python', [scriptPath, ...scriptArgs], { stdio: 'inherit', cwd: repoRoot });
  py.on('close', (code) => process.exit(code || 0));
}

if (!inRepo) {
  console.error('Run this CLI from a clone of https://github.com/seoskillsai/seo-skills-ai');
  process.exit(1);
}

if (action === 'doctor') {
  runPython('doctor.py');
} else if (action === 'setup') {
  runPython('setup_runtime.py');
} else if (action === 'audit') {
  if (!target) {
    console.error('Usage: audit <url>');
    process.exit(1);
  }
  runPython('full_audit.py', [target]);
} else if (action === 'fix') {
  if (!target) {
    console.error('Usage: fix <url>  (prints review-only patches; never writes the repo)');
    process.exit(1);
  }
  runPython('remediation_engine.py', [target]);
} else {
  console.error(`Unknown command: ${action}`);
  process.exit(1);
}
