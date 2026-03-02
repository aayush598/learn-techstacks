## 29. Streaming Responses in Express.js

**Streaming responses** in Express.js means sending data to the client **in small chunks as it becomes available**, instead of waiting for the entire response to be ready before sending it.

Streaming is essential for handling:

* Large files (videos, PDFs, ZIP files)
* Large datasets
* Real-time logs
* AI responses
* CSV exports
* Media content

Streaming improves **performance and memory efficiency**.

---

# 1. Normal Response vs Streaming Response

## Normal Response (Buffered)

Example:

```js
app.get('/data', async (req,res)=>{

 const data = await getLargeData();

 res.json(data);

});
```

Flow:

```
Server builds entire response
        ↓
Stored in memory
        ↓
Sent to client
```

Problems:

* High memory usage
* Slow response start
* Not scalable

---

## Streaming Response

Example:

```js
app.get('/stream',(req,res)=>{

 res.write("Part 1\n");

 setTimeout(()=>{
   res.write("Part 2\n");
   res.end();
 },2000);

});
```

Flow:

```
Send chunk 1
   ↓
Send chunk 2
   ↓
End response
```

Advantages:

* Low memory usage
* Faster response start
* Better scalability

---

# 2. How Streaming Works Internally

Node.js uses **streams**.

Streams process data in chunks.

Instead of:

```
Load entire data → Send
```

Streaming:

```
Chunk1 → Send
Chunk2 → Send
Chunk3 → Send
```

Express response object (`res`) is a writable stream.

Important methods:

```js
res.write()
res.end()
```

---

# 3. Basic Streaming Example

Example:

```js
app.get('/stream',(req,res)=>{

 res.write("Hello\n");

 setTimeout(()=>{
   res.write("World\n");
   res.end();
 },2000);

});
```

Output:

```
Hello
World
```

Client receives data gradually.

---

# 4. File Streaming (Most Common)

Very common interview topic.

Example:

```js
const fs = require('fs');

app.get('/download',(req,res)=>{

 const stream =
 fs.createReadStream('large.zip');

 stream.pipe(res);

});
```

Flow:

```
File Stream
    ↓
Pipe
    ↓
Response
```

Advantages:

* Uses very little memory
* Handles huge files
* Fast

---

# 5. Pipe Method

Most important concept.

```js
stream.pipe(res);
```

Meaning:

```
ReadStream → WriteStream
```

Equivalent to:

```
File → HTTP Response
```

Internally:

```
Read chunk
Write chunk
Repeat
```

---

# 6. Streaming Large Database Results

Bad approach:

```js
const users = await db.users.find();

res.json(users);
```

Problem:

```
Loads entire table
```

Better:

```js
dbStream.pipe(res);
```

Example concept:

```js
app.get('/users',(req,res)=>{

 const stream = db.queryStream();

 stream.pipe(res);

});
```

Used for:

* Large exports
* Analytics data

---

# 7. Streaming CSV Export

Example:

```js
app.get('/export',(req,res)=>{

 res.write("name,age\n");

 res.write("Aayush,22\n");

 res.write("John,30\n");

 res.end();

});
```

Client downloads progressively.

---

# 8. Setting Headers for Streaming

Example:

```js
app.get('/download',(req,res)=>{

 res.setHeader(
  "Content-Type",
  "application/octet-stream"
 );

 const stream =
 fs.createReadStream('large.zip');

 stream.pipe(res);

});
```

Important headers:

### Content-Type

Example:

```
application/pdf
video/mp4
text/csv
```

---

### Content-Disposition

For downloads:

```js
res.setHeader(
 "Content-Disposition",
 "attachment; filename=file.zip"
);
```

Browser downloads file.

---

# 9. Video Streaming (Advanced)

Example:

```js
app.get('/video',(req,res)=>{

 const stream =
 fs.createReadStream('video.mp4');

 res.setHeader("Content-Type","video/mp4");

 stream.pipe(res);

});
```

Used for:

* Video platforms
* Media services

---

# 10. Streaming vs Buffering

| Feature     | Buffering    | Streaming    |
| ----------- | ------------ | ------------ |
| Memory      | High         | Low          |
| Speed       | Slower start | Faster start |
| Large files | Bad          | Excellent    |
| Scalability | Poor         | Good         |

---

# 11. Real-Time Streaming (SSE)

Server-Sent Events example:

```js
app.get('/events',(req,res)=>{

 res.setHeader(
 "Content-Type",
 "text/event-stream"
 );

 setInterval(()=>{

  res.write(
   `data: ${Date.now()}\n\n`
  );

 },1000);

});
```

Client receives updates continuously.

Used for:

* Live dashboards
* Notifications
* AI streaming responses

---

# 12. Error Handling in Streams

Important production concept.

Example:

```js
app.get('/download',(req,res)=>{

 const stream =
 fs.createReadStream('file.zip');

 stream.on('error',(err)=>{
   res.status(500).send("Error");
 });

 stream.pipe(res);

});
```

Without handling:

```
Server crash possible
```

---

# 13. Backpressure (Advanced Concept)

Backpressure occurs when:

```
Client slow
Server fast
```

Streams automatically handle backpressure.

Example:

```
Pause reading
Resume reading
```

Pipe handles automatically.

---

# 14. When to Use Streaming

Use streaming for:

### Large Files

```
Video
PDF
ZIP
```

---

### Large Data

```
Millions of rows
```

---

### Real-Time Data

```
Logs
AI responses
Events
```

---

### Exports

```
CSV export
Reports
```

---

# 15. When NOT to Use Streaming

Avoid streaming for small responses:

```
User profile
Login response
Small JSON
```

Normal responses are simpler.

---

# 16. Typical Production Example

Example:

```js
app.get('/download',(req,res)=>{

 res.setHeader(
  "Content-Disposition",
  "attachment; filename=backup.zip"
 );

 const stream =
 fs.createReadStream('backup.zip');

 stream.pipe(res);

});
```

---

# 17. Common Interview Questions

## Question 1

Why streaming is better than sending full response?

Answer:

* Lower memory usage
* Faster response start
* Better scalability

---

## Question 2

Which method used for streaming?

Answer:

```js
res.write()
res.end()
```

or

```js
stream.pipe(res)
```

---

## Question 3

What is pipe()?

Answer:

Connects readable stream to writable stream.

---

## Question 4

Is res a stream?

Answer:

Yes.

```
res = writable stream
```

---

# Streaming Flow

```
Client Request
      ↓
Create Stream
      ↓
Pipe to Response
      ↓
Chunks Sent
      ↓
Response Ends
```

---

# Interview-Level Answer

**Streaming responses in Express.js involve sending data in chunks instead of sending the entire response at once. Since the Express response object is a writable stream, data can be sent using `res.write()` and `res.end()` or by piping readable streams like file streams using `stream.pipe(res)`. Streaming improves performance and reduces memory usage, making it ideal for large files, large datasets, and real-time data.**
