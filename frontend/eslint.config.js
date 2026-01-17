import js from "@eslint/js";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";

export default [
    js.configs.recommended,
    {
        files: ["**/*.{js,jsx,mjs,cjs,ts,tsx}"],
        plugins: {
            react,
            "react-hooks": reactHooks,
        },
        languageOptions: {
            parserOptions: {
                ecmaFeatures: {
                    jsx: true,
                },
            },
            globals: {
                ...globals.browser,
                ...globals.node,
                React: "readonly",
            },
        },
        rules: {
            "react/react-in-jsx-scope": "off",
            "no-unused-vars": "warn",
            ...reactHooks.configs.recommended.rules,
        },
        settings: {
            react: {
                version: "detect",
            },
        },
    },
];
