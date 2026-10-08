// Builds dist/index.js (ESM, React external) and dist/styles.css (tokens + era themes + components).
import { build } from 'esbuild';

await build({
  entryPoints: ['src/index.ts'],
  outfile: 'dist/index.js',
  bundle: true,
  format: 'esm',
  jsx: 'automatic',
  target: 'es2019',
  external: ['react', 'react/jsx-runtime', 'react-dom'],
  logLevel: 'info',
});

await build({
  entryPoints: ['src/styles.css'],
  outfile: 'dist/styles.css',
  bundle: true,
  logLevel: 'info',
});
