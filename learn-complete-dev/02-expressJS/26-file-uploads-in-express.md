## 26. File Uploads in Express.js

**File upload in Express.js** is the process of receiving files from a client (browser or API client) and storing or processing them on the server or a cloud service.

Express **does not support file uploads natively**, so middleware such as **Multer** is typically used to parse `multipart/form-data`.

---

# 1. How File Uploads Work

When a file is uploaded from a client, the request uses:

```http
Content-Type: multipart/form-data
```

Example request:

```http
POST /upload
Content-Type: multipart/form-data
```

Body structure:

```text
file: image.png
```

Express cannot parse this format using:

```js
express.json()
```

or

```js
express.urlencoded()
```

because file data is binary.

Middleware like **Multer** reads the request stream and extracts:

* Files → `req.file` or `req.files`
* Text fields → `req.body`

---

# 2. Multer Middleware

## Installation

```bash
npm install multer
```

---

## Basic File Upload Example

```js
const express = require('express');
const multer = require('multer');

const app = express();

const upload = multer({
  dest: 'uploads/'
});

app.post('/upload',
 upload.single('file'),
 (req,res)=>{

  res.send("File uploaded");

});
```

### Explanation

```js
upload.single('file')
```

* Accepts one file
* Field name = "file"

HTML form:

```html
<form method="POST" enctype="multipart/form-data">

<input type="file" name="file">

<button>Upload</button>

</form>
```

Uploaded file stored in:

```text
uploads/
```

---

# 3. File Object Structure

After upload:

```js
req.file
```

Example:

```js
{
 fieldname: 'file',
 originalname: 'image.png',
 encoding: '7bit',
 mimetype: 'image/png',
 destination: 'uploads/',
 filename: 'abc123.png',
 path: 'uploads/abc123.png',
 size: 34567
}
```

Important fields:

### originalname

```text
Original file name
```

---

### mimetype

```text
File type
```

Example:

```text
image/png
application/pdf
```

---

### path

```text
File location
```

---

### size

```text
File size in bytes
```

---

# 4. Upload Multiple Files

## Multiple Files Same Field

Example:

```js
app.post('/upload',
 upload.array('files',5),
 (req,res)=>{

 console.log(req.files);

 res.send("Uploaded");

});
```

Accepts:

```text
files[0]
files[1]
files[2]
```

Maximum:

```text
5 files
```

Stored in:

```js
req.files
```

---

# 5. Upload Multiple Fields

Example:

```js
const upload = multer({
 dest:'uploads/'
});

app.post('/upload',
 upload.fields([
   {name:'avatar',maxCount:1},
   {name:'resume',maxCount:1}
 ]),
 (req,res)=>{

 console.log(req.files);

});
```

Result:

```js
req.files.avatar
req.files.resume
```

---

# 6. Disk Storage Configuration

Custom storage configuration:

```js
const storage = multer.diskStorage({

 destination:(req,file,cb)=>{
   cb(null,'uploads/');
 },

 filename:(req,file,cb)=>{
   cb(null, Date.now()+"-"+file.originalname);
 }

});

const upload = multer({
 storage:storage
});
```

---

## Why Custom Filename Needed

Without it:

```text
Files may overwrite
```

Better:

```text
timestamp-file.png
```

---

# 7. Memory Storage

Stores file in RAM instead of disk.

Example:

```js
const storage = multer.memoryStorage();

const upload = multer({
 storage:storage
});
```

File stored as:

```js
req.file.buffer
```

Used for:

* AWS S3 upload
* Cloudinary upload
* Image processing

---

# 8. Upload to Cloud Storage

Example (concept):

```js
app.post('/upload',
 upload.single('file'),
 async(req,res)=>{

 const buffer = req.file.buffer;

 await uploadToCloud(buffer);

 res.send("Uploaded");

});
```

Used in production systems.

---

# 9. File Type Filtering

Important for security.

Example:

```js
const upload = multer({

 dest:'uploads/',

 fileFilter:(req,file,cb)=>{

  if(file.mimetype === 'image/png' ||
     file.mimetype === 'image/jpeg'){

     cb(null,true);

  }else{

     cb(new Error("Invalid file type"));

  }

 }

});
```

Allows:

```text
PNG
JPEG
```

Blocks:

```text
.exe
.js
.zip
```

---

# 10. File Size Limits

Important for security.

Example:

```js
const upload = multer({

 dest:'uploads/',

 limits:{
   fileSize: 5 * 1024 * 1024
 }

});
```

Limit:

```text
5 MB
```

Prevents:

```text
Huge file attacks
```

---

# 11. Handling Upload Errors

Example:

```js
app.post('/upload',
 upload.single('file'),
 (req,res)=>{

 res.send("OK");

});
```

Error handler:

```js
app.use((err,req,res,next)=>{

 res.status(400).json({
   error:err.message
 });

});
```

---

# 12. File Upload Flow

Flow:

```text
Client Upload
   ↓
multipart/form-data request
   ↓
Multer Middleware
   ↓
Parse stream
   ↓
Save file / memory
   ↓
req.file
   ↓
Route Handler
```

---

# 13. Production Best Practices

## 1. Validate File Types

```js
fileFilter
```

---

## 2. Limit File Size

```js
limits.fileSize
```

---

## 3. Use Unique Filenames

```js
Date.now()
uuid()
```

---

## 4. Use Cloud Storage

Better than local storage:

* AWS S3
* Cloudinary
* GCP Storage

---

## 5. Avoid Public Upload Folder

Better:

```text
private/uploads
```

---

# 14. Streaming Uploads (Advanced)

For large files:

```text
Video uploads
Large datasets
```

Better to stream instead of buffering.

Example concept:

```js
req.pipe(writeStream);
```

Uses less memory.

---

# 15. Common Interview Questions

## Question 1

Why Express cannot upload files directly?

Answer:

Because:

```text
multipart/form-data must be parsed
```

Express only handles JSON and URL encoded.

---

## Question 2

Difference between diskStorage and memoryStorage?

diskStorage:

```text
Stored on disk
```

memoryStorage:

```text
Stored in RAM
```

---

## Question 3

Where file stored after upload?

Answer:

```js
req.file
req.files
```

---

## Question 4

How to upload multiple files?

Answer:

```js
upload.array('files')
```

---

# Interview-Level Answer

**File uploads in Express are handled using middleware like Multer, which parses multipart/form-data requests and extracts files into `req.file` or `req.files`. Multer can store files either on disk using diskStorage or in memory using memoryStorage. File uploads should include validation for file types and size limits for security and performance.**

---

Next section:

**Advanced Express**

27. Rate limiting
28. Large payload handling
29. Streaming responses
30. Timeouts and retries

These are **very high-value backend interview topics.**
