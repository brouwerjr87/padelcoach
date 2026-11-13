// node bouw.js in.html uit.html technieken.json houdingen3d.json
// Zet de inhoud (teksten en houdingen) terug in de gebouwde app.
const fs = require('fs')
const [inp, uit, tj, hj] = process.argv.slice(2)
let b = fs.readFileSync(inp, 'utf8')
function litEnd(start) { let i = start + 1; for (;;) { if (b[i] === '\\') { i += 2; continue } if (b[i] === '`') return i; i++ } }
// technieken: C=JSON.parse(`...`)
const k = b.indexOf('C=JSON.parse(`'); if (k < 0) throw new Error('technieken niet gevonden')
const s0 = k + 13, e0 = litEnd(s0)
const T = JSON.parse(fs.readFileSync(tj, 'utf8'))
const esc = JSON.stringify(T).replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$\{/g, '\\${')
b = b.slice(0, s0) + '`' + esc + '`' + b.slice(e0 + 1)
// houdingen: het objectliteraal rond "fh-volley-raak":{bekken
const m = /"fh-volley-raak":\{"?bekken/.exec(b); if (!m) throw new Error('houdingen niet gevonden'); const h = m.index
let d = 0, i = h; for (; i > 0; i--) { const c = b[i]; if (c === '}') d++; else if (c === '{') { if (d === 0) break; d-- } }
let j = i, dd = 0; for (; j < b.length; j++) { const c = b[j]; if (c === '{') dd++; else if (c === '}') { dd--; if (dd === 0) break } }
const H = JSON.parse(fs.readFileSync(hj, 'utf8'))
b = b.slice(0, i) + JSON.stringify(H) + b.slice(j + 1)
fs.writeFileSync(uit, b)
console.log('geschreven', uit, b.length)
