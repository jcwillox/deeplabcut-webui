/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/eslint-config-typescript/recommended"
  ],
  env: {
    "vue/setup-compiler-macros": true
  },
  rules: {
    "@typescript-eslint/no-non-null-assertion": "off"
  },
  globals: {
    DOMHighResTimeStamp: true,
    VideoFrameMetadata: true,
    $: true,
    $$: true,
    $ref: true,
    $shallowRef: true,
    $computed: true,
    $customRef: true,
    $toRef: true
  }
};
