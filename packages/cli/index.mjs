#!/usr/bin/env node
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const action = args[0];
const target = args[1];
const here = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(here, '..', '..');
const VERSION = '1.2.1';

function exists(p) {
  try {
    fs.accessSync(p);
    return true;
  } catch {
    return false;
  }
}

function copyIntoWorkspace(destRoot) {
  const mapping = [
    ['AGENTS.md', 'AGENTS.md'],
    ['.cursorrules', '.cursorrules'],
    ['.claude-plugin', '.claude-plugin'],
    ['.codex-plugin', '.codex-plugin'],
    ['skills', 'skills'],
    ['scripts', 'scripts'],
    ['agents', 'agents'],
    ['hooks', 'hooks'],
  ];
  const copied = [];
  for (const [rel, destName] of mapping) {
    const src = path.join(pkgRoot, rel);
    if (!exists(src)) continue;
    const dest = path.join(destRoot, destName);
    fs.cpSync(src, dest, { recursive: true });
    copied.push(destName);
  }
  return copied;
}

console.log(`[seoskillsai CLI] SEO Skills AI v${VERSION}`);

if (!action || action === 'help' || action === '--help') {
  console.log(`
Install into the current workspace (copies skills, scripts, AGENTS.md from this package):

  npx @seoskillsai/cli add cursor

Then open that folder as the agent workspace.

Commands:
  add <cursor|claude|codex|all>   Copy package contents into cwd
  doctor                          python scripts/doctor.py
  setup                           python scripts/setup_runtime.py
  audit <url>                     python scripts/full_audit.py <url>
  fix <url>                       python scripts/remediation_engine.py <url> (review-only)
`);
  process.exit(0);
}

if (action === 'add') {
  const dest = process.cwd();
  if (!exists(path.join(pkgRoot, 'AGENTS.md')) || !exists(path.join(pkgRoot, 'skills'))) {
    console.error('Package is missing AGENTS.md/skills. Reinstall @seoskillsai/cli.');
    process.exit(1);
  }
  const copied = copyIntoWorkspace(dest);
  if (!copied.length) {
    console.error('Nothing was copied. The npm package files list is incomplete.');
    process.exit(1);
  }
  console.log(`Copied into ${dest}: ${copied.join(', ')}`);
  console.log(`Open this folder as the ${target || 'agent'} workspace.`);
  process.exit(0);
}

function runPython(scriptName, scriptArgs = []) {
  const scriptPath = path.join(pkgRoot, 'scripts', scriptName);
  if (!exists(scriptPath)) {
    console.error(`Missing ${scriptPath}. Run from a clone or after npx @seoskillsai/cli add.`);
    process.exit(1);
  }
  const py = spawn('python', [scriptPath, ...scriptArgs], { stdio: 'inherit', cwd: process.cwd() });
  py.on('close', (code) => process.exit(code || 0));
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
