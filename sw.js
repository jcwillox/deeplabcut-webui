if(!self.define){let e,s={};const i=(i,n)=>(i=new URL(i+".js",n).href,s[i]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=s,document.head.appendChild(e)}else e=i,importScripts(i),s()})).then((()=>{let e=s[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(n,r)=>{const o=e||("document"in self?document.currentScript.src:"")||location.href;if(s[o])return;let t={};const l=e=>i(e,o),d={module:{uri:o},exports:t,require:l};s[o]=Promise.all(n.map((e=>d[e]||l(e)))).then((e=>(r(...e),t)))}}define(["./workbox-4ee7f24a"],(function(e){"use strict";self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"assets/index.92f9ce9a.js",revision:null},{url:"assets/index.e4dd5b6e.css",revision:null},{url:"assets/webfontloader.ccf6ba4d.js",revision:null},{url:"index.html",revision:"0b9209079b0b840a8175e49dc4bd5dd8"},{url:"icon.svg",revision:"ffda5819c9956cd53da1280288f8f770"},{url:"icon-192.png",revision:"5b96aee4b9351cd5f55bb740d0ca2285"},{url:"icon-512.png",revision:"5f416921f5febbf7c8064a411838ad4e"},{url:"manifest.webmanifest",revision:"c15bf533e36a4a1f24887b0cb6354079"}],{}),e.cleanupOutdatedCaches(),e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html"),{denylist:[/^.*\/docs.*$/]}))}));
