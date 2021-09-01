let timestamp = Date.now();
let love = "❤";
let smile = "\u{1F600}";
let cross = "\u2718"
let sym = Symbol.for("lll")
console.log("  \u{1F600} ", "\f \b \v", love.repeat(5));
let symname = Symbol("propname");
let errorMessage = `\
Test failure at ${love}:${smile}:
${cross} &", ${symname}, " & ", ${sym} `

console.log(timestamp);
let greeting = "Welcome to my blog," + " ";
let now = new Date();
console.log(now)
let ms = now.getTime();
console.log(ms)
let iso = now.toISOString();
console.log(iso, errorMessage);