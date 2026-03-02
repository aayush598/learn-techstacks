## 28. How to Handle Large Payloads in Express.js

**Handling large payloads** in Express.js means safely processing **large request bodies or responses** such as:

* Large JSON requests (5–100 MB)
* File uploads (images, videos)
* CSV or Excel imports
* Logs or analytics data
* Media content

Improper handling of large payloads can cause:

* High memory usage
* Slow server performance
* Server crashes
* Denial-of-service vulnerabilities

---

# 1. Problems with Large Payloads

Example large request:

```text
POST /data
Content-Length: 50MB
```

If Express tries to parse this using:

```js
app.use(express.json());
```

Problems:

### 1. High Memory Usage

Express loads the entire payload into memory before parsing.

```text
50MB request → 50MB RAM usage
```

Multiple requests:

```text
50MB × 20 users = 1GB RAM
```

Server crash possible.

---

### 2. Slow Parsing

JSON parsing is CPU intensive.

```js
JSON.parse(largeObject)
```

Large objects slow the event loop.

---

### 3. Security Risks

Attack example:

```text
POST /users
Body: 500MB JSON
```

Result:

```text
Server out of memory
```

This is a type of **DoS attack.**

---

# 2. Limit Request Size (Most Important)

First step in production.

Example:

```js
app.use(express.json({
 limit: "1mb"
}));
```

Meaning:

```text
Max request size = 1MB
```

If exceeded:

```http
413 Payload Too Large
```

---

## URL Encoded Limit

```js
app.use(express.urlencoded({
 extended: true,
 limit: "1mb"
}));
```

---

## Example Production Setup

```js
app.use(express.json({
 limit: "2mb"
}));

app.use(express.urlencoded({
 extended:true,
 limit:"2mb"
}));
```

---

# 3. Use Streaming Instead of Buffering

Best approach for very large data.

Instead of:

```text
Load entire file into memory
```

Use:

```text
Process chunk by chunk
```

---

## Example File Streaming

```js
const fs = require('fs');

app.get('/download',(req,res)=>{

 const stream =
 fs.createReadStream('bigfile.zip');

 stream.pipe(res);

});
```

Advantages:

* Low memory usage
* Faster start
* Scalable

---

# 4. Stream Large Uploads

Example concept:

```js
req.pipe(writeStream);
```

Instead of:

```js
req.body
```

Flow:

```text
Client Upload
   ↓
Stream chunks
   ↓
Write to disk
```

Uses minimal RAM.

---

# 5. Use Multer for File Uploads

Large files handled using multipart streams.

Example:

```js
const multer = require('multer');

const upload = multer({
 dest:'uploads/',
 limits:{
  fileSize:50*1024*1024
 }
});

app.post('/upload',
 upload.single('file'),
 handler);
```

Limits:

```text
50 MB max
```

---

# 6. Compression Middleware

Reduces payload size.

Install:

```bash
npm install compression
```

Example:

```js
const compression=require('compression');

app.use(compression());
```

Reduces:

```text
Response size
```

Example:

```text
1MB JSON → 200KB compressed
```

---

# 7. Reverse Proxy Limits (Important)

Usually Express runs behind NGINX.

NGINX limit:

```text
client_max_body_size 10M;
```

If exceeded:

```http
413 Request Entity Too Large
```

Better to limit at proxy and app both.

---

# 8. Avoid Large JSON When Possible

Bad design:

```json
{
 "users":[ 1 million users ]
}
```

Better:

```text
Pagination
```

Example:

```text
GET /users?page=1&limit=50
```

---

# 9. Chunk Processing

Process in pieces.

Example:

```text
Large CSV file
```

Instead of:

```text
Load entire CSV
```

Better:

```text
Read line-by-line
```

Libraries:

* csv-parser
* fast-csv

---

# 10. Background Processing

Large data tasks should not block API.

Example:

```text
Upload video
Process video
```

Better:

```text
Upload → Queue → Worker
```

Tools:

* BullMQ
* RabbitMQ

---

# 11. Timeout Protection

Large payloads take time.

Example:

```js
server.setTimeout(10000);
```

Prevents:

```text
Hanging requests
```

---

# 12. Validate Payload Early

Check headers first.

Example:

```js
app.use((req,res,next)=>{

 const length = req.headers['content-length'];

 if(length > 5*1024*1024){
   return res.status(413).send();
 }

 next();

});
```

Rejects early.

---

# 13. Database Considerations

Avoid:

```text
Huge inserts in one request
```

Better:

```text
Batch inserts
```

Example:

```text
1000 rows per batch
```

---

# 14. Typical Production Setup

Example:

```js
app.use(express.json({
 limit:"2mb"
}));

app.use(express.urlencoded({
 extended:true,
 limit:"2mb"
}));

app.use(compression());
```

Uploads:

```js
const upload=multer({

 limits:{
   fileSize:20*1024*1024
 }

});
```

---

# 15. Best Practices Summary

## 1. Always Limit Size

```js
limit:"1mb"
```

---

## 2. Use Streaming for Large Files

```js
stream.pipe(res)
```

---

## 3. Use Pagination

Avoid huge responses.

---

## 4. Use Compression

```js
compression()
```

---

## 5. Use Reverse Proxy Limits

NGINX protection.

---

## 6. Use Background Jobs

Heavy processing outside API.

---

# 16. Common Interview Questions

## Question 1

What happens with large JSON?

Answer:

* High memory usage
* Slow parsing
* Possible crash

---

## Question 2

Best method for large files?

Answer:

```text
Streaming
```

---

## Question 3

How to protect server?

Answer:

```text
Request size limits
```

---

## Question 4

Why streaming better?

Answer:

```text
Low memory usage
```

---

# Request Flow Example

```text
Client Request
    ↓
Size Limit Check
    ↓
Allowed
    ↓
Stream or Parse
    ↓
Handler
```

---

# Interview-Level Answer

**Large payloads in Express should be handled by limiting request sizes using middleware like `express.json({limit:"1mb"})`, using streaming for large files instead of buffering them into memory, and applying file size limits for uploads. Additional strategies include compression, pagination, and reverse proxy limits to prevent excessive memory usage and denial-of-service attacks.**
