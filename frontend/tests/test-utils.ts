import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export function loadTemplate(relativePath: string): string {
  return readFileSync(join(__dirname, relativePath), 'utf-8');
}

export function loadStyle(relativePath: string): string {
  return readFileSync(join(__dirname, relativePath), 'utf-8');
}
