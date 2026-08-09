import { defineConfig } from 'vite';

// base must match the GitHub Pages repo path, e.g. https://user.github.io/peripheral/
// If you deploy to a user/organization root page instead, set this to '/'.
export default defineConfig({
  base: '/peripheral/',
  build: {
    target: 'es2020',
    // Everything is generated in code, so the bundle is the whole game.
    assetsInlineLimit: 0,
  },
});
