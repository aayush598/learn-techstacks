## 30. Handling Timeouts and Retries in Express.js

**Timeouts and retries** are techniques used to ensure that an Express.js application remains **reliable and responsive** when operations take too long or fail temporarily.

They help handle:

* Slow database queries
* External API delays
* Network failures
* Hanging requests
* Temporary service outages

Without timeouts and retries:

```text
Client → Request → Server waits forever → Client stuck
```

With timeouts:

```text
Client → Request → Timeout → Error response
```

With retries:

```text
Client → Request → Failure → Retry → Success
```

---

# 1. What is a Timeout?

A **timeout** is the maximum time the server waits before terminating a request.

Example:

```text
API timeout = 5 seconds
```

If the request takes longer:

```http
408 Request Timeout
```

or

```http
504 Gateway Timeout
```

---

# 2. Why Timeouts Are Important

Without timeouts:

Problems:

### 1. Hanging Requests

Example:

```text
Database never responds
```

Result:

```text
Connection stuck forever
```

---

### 2. Resource Exhaustion

Example:

```text
1000 hanging requests
```

Result:

```text
Server memory exhausted
```

---

### 3. Poor User Experience

Example:

```text
Frontend waits 60 seconds
```

Bad UX.

---

# 3. Server-Level Timeout

Node.js server timeout.

Example:

```js
const server = app.listen(3000);

server.setTimeout(5000);
```

Meaning:

```text
Request must complete within 5 seconds
```

Otherwise connection closed.

---

# 4. Response Timeout Middleware

Example:

```js
app.use((req,res,next)=>{

 res.setTimeout(5000,()=>{

   res.status(408).send("Request Timeout");

 });

 next();

});
```

Meaning:

```text
If response takes >5 sec → timeout
```

---

# 5. Timeout for Specific Routes

Better approach.

Example:

```js
app.get('/reports',(req,res)=>{

 res.setTimeout(10000);

 generateReport(res);

});
```

Long-running route allowed more time.

---

# 6. Timeout for External APIs

Very common interview question.

Example using fetch/axios.

Axios example:

```js
const axios = require('axios');

axios.get("https://api.example.com",{
 timeout:5000
});
```

Meaning:

```text
Cancel request after 5 sec
```

---

# 7. AbortController Timeout (Modern Method)

Example:

```js
const controller =
 new AbortController();

setTimeout(()=>{
 controller.abort();
},5000);

fetch(url,{
 signal:controller.signal
});
```

Cancels request after timeout.

---

# 8. Retry Mechanism

Retries attempt the request again if it fails.

Example:

```text
Attempt 1 → Fail
Attempt 2 → Fail
Attempt 3 → Success
```

Useful for:

* Network errors
* Temporary outages
* Rate limits
* Cloud services

---

# 9. Basic Retry Implementation

Example:

```js
async function retry(fn,retries=3){

 try{

  return await fn();

 }
 catch(err){

  if(retries === 0){
    throw err;
  }

  return retry(fn,retries-1);

 }

}
```

Usage:

```js
await retry(()=>{
 return axios.get(url);
});
```

---

# 10. Retry With Delay

Better approach.

Example:

```js
async function retry(fn,retries=3,delay=1000){

 try{

  return await fn();

 }
 catch(err){

  if(retries===0)
    throw err;

  await new Promise(r=>setTimeout(r,delay));

  return retry(fn,retries-1,delay);

 }

}
```

Flow:

```text
Attempt 1
 ↓
Wait 1 sec
 ↓
Attempt 2
 ↓
Wait 1 sec
 ↓
Attempt 3
```

---

# 11. Exponential Backoff (Production Standard)

Better retry strategy.

Example:

```text
Attempt 1 → wait 1 sec
Attempt 2 → wait 2 sec
Attempt 3 → wait 4 sec
```

Example:

```js
async function retry(fn,retries=3){

 try{

  return await fn();

 }
 catch(err){

  if(retries===0)
   throw err;

  const delay =
   Math.pow(2,3-retries)*1000;

  await new Promise(
   r=>setTimeout(r,delay)
  );

  return retry(fn,retries-1);

 }

}
```

---

# 12. When to Retry

Safe to retry:

### Network Errors

```text
Connection reset
Timeout
DNS error
```

---

### Temporary Failures

```text
503 Service Unavailable
```

---

### Rate Limit

```text
429 Too Many Requests
```

After delay.

---

# 13. When NOT to Retry

Do NOT retry:

### Bad Request

```http
400 Bad Request
```

---

### Unauthorized

```http
401 Unauthorized
```

---

### Validation Errors

Retry will fail again.

---

# 14. Combining Timeout + Retry

Best practice.

Example:

```js
await retry(()=>{

 return axios.get(url,{
  timeout:3000
 });

},3);
```

Flow:

```text
Attempt1 → Timeout
Attempt2 → Timeout
Attempt3 → Success
```

---

# 15. Production Best Practices

## Use Timeouts Everywhere

* API requests
* DB queries
* External services

---

## Use Retry Carefully

Too many retries:

```text
More server load
```

Best:

```text
3 retries max
```

---

## Log Failures

Example:

```js
console.error(err);
```

---

## Return Clear Errors

Example:

```json
{
 "error":"Service unavailable"
}
```

---

# 16. Typical Production Setup

Example:

```js
server.setTimeout(10000);
```

External APIs:

```js
axios.get(url,{
 timeout:5000
});
```

Retry:

```text
3 attempts
```

---

# 17. Common Interview Questions

## Question 1

Why timeouts needed?

Answer:

* Prevent hanging requests
* Protect resources

---

## Question 2

Where apply timeouts?

Answer:

* Server
* External APIs
* DB queries

---

## Question 3

Best retry strategy?

Answer:

```text
Exponential backoff
```

---

## Question 4

Should we retry POST requests?

Answer:

Usually no.

Because:

```text
May create duplicates
```

---

# Request Flow

```text
Client Request
     ↓
Start Timer
     ↓
Operation
     ↓
Success → Response

OR

Timeout → Error
     ↓
Retry
     ↓
Success or Fail
```

---

# Interview-Level Answer

**Handling timeouts and retries in Express involves setting maximum request durations using server or middleware timeouts and retrying failed operations such as external API calls using controlled retry strategies. Timeouts prevent hanging requests and resource exhaustion, while retries with exponential backoff improve reliability during temporary failures. Timeouts are typically applied to server requests and external APIs, and retries are used mainly for network or transient errors.**
