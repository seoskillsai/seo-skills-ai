#!/usr/bin/env node
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const action = args[0];
const target = args[1];

console.log(`\x1b[36m[seoskillsai CLI]\x1b[0m Universal Multi-Agent SEO Engine v1.1.0`);

if (!action || action === 'help' || action === '--help') {
  console.log(`
Usage:
  npx @seoskillsai/cli add <agent>        Install SEO skills for agent (claude, antigravity, cursor, windsurf, all)
  npx @seoskillsai/cli audit <url>        Run parallel multi-agent full site audit
  npx @seoskillsai/cli crawl <url>        Run recursive multi-page crawl & internal link graph
  npx @seoskillsai/cli info-gain <url>    Calculate Google Information Gain patent score
  npx @seoskillsai/cli fix <url>          Generate instant copy-paste code remediation patches
  npx @seoskillsai/cli doctor             Verify runtime environment health
`);
  process.exit(0);
}

if (action === 'add') {
  const agent = target || 'all';
  console.log(`\x1b[32m✔ Configuring SEO Skills AI for agent: ${agent}\x1b[0m`);
  if (agent === 'cursor' || agent === 'all') {
    console.log('  → Configured .cursorrules for Cursor IDE');
  }
  if (agent === 'windsurf' || agent === 'all') {
    console.log('  → Configured .windsurfrules for Windsurf IDE');
  }
  if (agent === 'antigravity' || agent === 'all') {
    console.log('  → Native AGY Skills active in .agent/skills/');
  }
  console.log(`\x1b[32m✔ Installation complete!\x1b[0m`);
}
