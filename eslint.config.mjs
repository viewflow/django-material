// eslint.config.mjs
import js from '@eslint/js';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['material/templates/cotton/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        up: 'readonly'
      }
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'warn'
    }
  }
];