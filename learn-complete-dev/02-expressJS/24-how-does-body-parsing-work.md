## 24. How Body Parsing Works in Express.js

**Body parsing** is the process of reading and converting the **HTTP request body (raw data stream)** into a usable JavaScript object and attaching it to `req.body`.

Without body parsing, Express **cannot read POST/PUT request data properly.**

---

# 1. What is Request Body?

The **request body** contains data sent by the client, usually in:

* JSON
* Form data
* URL-encoded data
* Multipart data (file uploads)

Example HTTP request:

```http
POST /users
Content-Type: application/json

{
  "name": "Aayush",
  "age": 22
}
```

The JSON part is the **request body**.

---

# 2. Why Body Parsing is Needed

Node.js receives the request body as a **raw stream of bytes**, not a JavaScript object.

Without body parsing:

```js
app.post('/users', (req,res)=>{
 console.log(req.body);
});
```

Output:

```text
undefined
```

Because Express has not parsed the body.

---

# 3. express.json() Middleware

Express provides built-in middleware:

```js
app.use(express.json());
```

This middleware:

1. Reads request stream
2. Collects data chunks
3. Converts JSON string → JavaScript object
4. Stores in `req.body`

Example:

```js
const express = require('express');

const app = express();

app.use(express.json());

app.post('/users',(req,res)=>{

 console.log(req.body);

 res.send("OK");

});
```

Request:

```json
{
 "name":"Aayush"
}
```

Output:

```js
{ name: "Aayush" }
```

---

# 4. Internal Working (Important Interview Topic)

## Step 1 — Request Arrives

Client sends request:

```http
POST /users
```

Body:

```json
{"name":"Aayush"}
```

---

## Step 2 — Node.js Receives Stream

Node HTTP server receives body as **chunks.**

Example conceptually:

```text
Chunk 1 → {"na
Chunk 2 → me":"A
Chunk 3 → ayush"}
```

Node provides:

```js
req.on('data', chunk => {})
req.on('end', ()=>{})
```

Example raw Node.js:

```js
req.on('data',(chunk)=>{
 body += chunk;
});

req.on('end',()=>{
 console.log(body);
});
```

Output:

```text
{"name":"Aayush"}
```

Still string.

---

## Step 3 — Express Parser Converts Data

express.json():

* Reads stream
* Combines chunks
* Converts using JSON.parse()

Equivalent to:

```js
const obj = JSON.parse(body);
```

---

## Step 4 — Data Stored in req.body

Final object:

```js
req.body = {
 name:"Aayush"
}
```

---

# 5. express.urlencoded()

Used for HTML form submissions.

Example form:

```html
<form method="POST">

<input name="name">
<input name="age">

</form>
```

Request body:

```text
name=Aayush&age=22
```

Parser:

```js
app.use(express.urlencoded({
 extended:true
}));
```

Result:

```js
req.body = {
 name:"Aayush",
 age:"22"
}
```

---

# 6. extended:true vs false

## extended:false

Uses simple parser.

Supports:

```text
name=Aayush
```

---

## extended:true

Uses **qs library**

Supports nested objects:

```text
user[name]=Aayush
```

Parsed:

```js
{
 user:{
  name:"Aayush"
 }
}
```

Best practice:

```js
extended:true
```

---

# 7. Body Parsing Limit

Important for security.

Example:

```js
app.use(express.json({
 limit:"1mb"
}));
```

Prevents:

```text
Huge request attacks
```

Example attack:

```text
500MB JSON request
```

Could crash server.

---

# 8. Content-Type Matters

Body parser works only if **Content-Type matches.**

Example JSON:

```http
Content-Type: application/json
```

If wrong:

```http
Content-Type: text/plain
```

Result:

```text
req.body = undefined
```

---

# 9. Multiple Parsers

Typical production setup:

```js
app.use(express.json());

app.use(express.urlencoded({
 extended:true
}));
```

Supports:

```text
JSON requests
Form requests
```

---

# 10. Multipart Data (File Uploads)

express.json() cannot parse files.

Example:

```text
multipart/form-data
```

Need multer.

Example:

```js
const multer=require('multer');

const upload=multer();

app.post('/upload',
 upload.single('file'),
(req,res)=>{

 console.log(req.file);

});
```

---

# 11. Raw Body Parsing

Sometimes needed:

Example:

```text
Webhook verification
Stripe
Razorpay
```

Parser:

```js
app.use(express.raw({
 type:'application/json'
}));
```

Provides:

```js
req.body → Buffer
```

---

# 12. Text Body Parsing

Example:

```js
app.use(express.text());
```

Request:

```text
Hello world
```

Result:

```js
req.body = "Hello world"
```

---

# 13. Middleware Order Matters

Correct:

```js
app.use(express.json());

app.post('/users', handler);
```

Wrong:

```js
app.post('/users', handler);

app.use(express.json());
```

Then:

```text
req.body = undefined
```

---

# 14. Performance Considerations

Body parsing:

* Uses memory
* CPU for JSON.parse()

Large JSON → slow.

Better approach:

```text
Use streaming
```

For:

* CSV
* Videos
* Logs

---

# 15. Security Considerations

## Limit Size

```js
limit:"1mb"
```

---

## Validate Input

Never trust req.body.

Example:

```js
if(!req.body.email)
 return res.status(400);
```

---

# 16. Common Interview Questions

## Question 1

What happens without express.json()?

Answer:

```text
req.body is undefined
```

---

## Question 2

How does Express parse body internally?

Answer:

1 Receive stream
2 Combine chunks
3 JSON.parse()
4 Attach to req.body

---

## Question 3

Why body parser needed?

Answer:

Node.js receives raw stream, not object.

---

## Question 4

Difference between json and urlencoded?

json:

```json
{"name":"Aayush"}
```

urlencoded:

```text
name=Aayush
```

---

# Request Flow Diagram

```text
Client Request
   ↓
Raw Data Stream
   ↓
express.json()
   ↓
JSON.parse()
   ↓
req.body
   ↓
Route Handler
```

---

# Interview-Level Answer

**Body parsing in Express is the process of reading the incoming HTTP request body stream and converting it into a usable JavaScript object stored in `req.body`. Middleware like `express.json()` reads incoming data chunks, combines them into a string, parses the JSON using `JSON.parse()`, and attaches the result to the request object. Without body parsing middleware, `req.body` remains undefined.**
