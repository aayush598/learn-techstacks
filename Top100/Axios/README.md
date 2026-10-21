# Axios Interview Questions and Answers

## Q1: What is Axios?
**A:** Axios is a promise-based HTTP client for JavaScript that works in both browser and Node.js environments. It provides a simple API for making HTTP requests (GET, POST, PUT, DELETE, etc.), automatic JSON parsing, request/response interception, and error handling.

## Q2: How do you install Axios?
**A:** Install via npm: `npm install axios`. For browser via CDN: `<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>`. Axios can also be imported as a module: `import axios from 'axios'`.

## Q3: How do you make a GET request with Axios?
**A:** `axios.get('/api/users', { params: { page: 1 } }).then(response => console.log(response.data)).catch(error => console.error(error))`. The response object contains `data`, `status`, `statusText`, `headers`, and `config`.

## Q4: How do you make a POST request with Axios?
**A:** `axios.post('/api/users', { name: 'John', email: 'john@example.com' }, { headers: { 'Content-Type': 'application/json' } }).then(res => console.log(res.data))`. The second argument is the request body, the third is config.

## Q5: How do you make a PUT request with Axios?
**A:** `axios.put('/api/users/1', { name: 'John Updated' }).then(res => console.log(res.data))`. Similar to POST but semantically for updating resources. Also: `axios.patch()` for partial updates.

## Q6: How do you make a DELETE request with Axios?
**A:** `axios.delete('/api/users/1').then(res => console.log('Deleted')).catch(err => console.error(err))`. DELETE requests can have a config object as the second argument for headers, params, etc.

## Q7: What is the Axios response object structure?
**A:** The response object contains: `data` (parsed response body), `status` (HTTP status code), `statusText` (status message), `headers` (response headers), `config` (request configuration), `request` (the XMLHttpRequest or Node.js request object).

## Q8: What is the Axios error object structure?
**A:** The error object contains: `message` (error description), `response` (response object if server responded), `request` (request object if no response), `config` (request configuration), `code` (error code like ERR_NETWORK, ERR_TIMEOUT). Check `error.response` for server errors.

## Q9: How do you set default configuration for Axios?
**A:** `axios.defaults.baseURL = 'https://api.example.com'`; `axios.defaults.headers.common['Authorization'] = AUTH_TOKEN`; `axios.defaults.timeout = 5000`. Defaults apply to all requests. Can also set `headers.post`, `headers.put`, etc.

## Q10: How do you create an Axios instance?
**A:** `const api = axios.create({ baseURL: 'https://api.example.com', timeout: 5000, headers: { 'X-Custom': 'value' } })`. Instances have independent configuration while sharing the same API methods. Useful for different API endpoints or auth contexts.

## Q11: Why use Axios instances?
**A:** Instances provide isolated configuration for different API services. Each instance can have its own baseURL, interceptors, headers, and auth tokens. Prevents mixing configurations between different backends (e.g., auth API vs main API).

## Q12: How do you use interceptors in Axios?
**A:** `axios.interceptors.request.use(config => { config.headers.Authorization = `Bearer ${token}`; return config }, error => Promise.reject(error))`. Response interceptors: `axios.interceptors.response.use(response => response, error => handleError(error))`.

## Q13: What is a request interceptor?
**A:** A function that runs before each request is sent. Used for: adding auth tokens, logging requests, modifying request config (headers, params), transforming request data. Runs in order of registration. Returns the modified config or a rejected promise.

## Q14: What is a response interceptor?
**A:** A function that runs when a response is received. Used for: transforming response data, handling global errors (401 redirect to login), logging responses, refreshing tokens on 401. The success handler receives the response; the error handler receives the error.

## Q15: How do you remove interceptors?
**A:** Store the interceptor ID: `const id = axios.interceptors.request.use(handler)`. Remove with `axios.interceptors.request.eject(id)`. Or use `axios.interceptors.request.clear()` to remove all.

## Q16: How do you handle authentication with Axios?
**A:** Common patterns: set a token in request interceptor, use `withCredentials: true` for cookies, pass token in headers manually per request. Token refresh is typically handled in a response interceptor by retrying the failed request.

## Q17: How do you refresh expired tokens with Axios?
**A:** In the response interceptor, catch 401 errors. If it's not a retry, call the refresh endpoint, update the token, and retry the original request (`axios(config)`). Use a queue to prevent multiple simultaneous refresh calls.

## Q18: How do you cancel a request in Axios?
**A:** Use `AbortController` (Axios v0.22+): `const controller = new AbortController(); axios.get('/api/data', { signal: controller.signal }); controller.abort()`. The request promise rejects with a CanceledError.

## Q19: How do you handle request timeouts in Axios?
**A:** Set `timeout` in config: `axios.get('/api/data', { timeout: 5000 })`. The request is aborted after 5 seconds. `timeoutErrorMessage` customizes the error message. Handle in catch: `if (error.code === 'ECONNABORTED')`.

## Q20: How does Axios handle concurrent requests?
**A:** Use `axios.all([request1, request2])` with `axios.spread((res1, res2) => { ... })` (legacy). Modern: use `Promise.all([axios.get('/api/1'), axios.get('/api/2')])` directly since Axios returns Promises.

## Q21: How do you upload files with Axios?
**A:** Use FormData: `const formData = new FormData(); formData.append('file', fileInput.files[0]); axios.post('/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })`. Axios automatically sets Content-Type with boundary for FormData.

## Q22: How do you track upload progress with Axios?
**A:** Use `onUploadProgress` in config: `axios.post('/upload', formData, { onUploadProgress: (progressEvent) => { const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total); console.log(`${percent}%`) } })`. Also `onDownloadProgress` for download progress.

## Q23: How do you track download progress with Axios?
**A:** `axios.get('/large-file', { responseType: 'stream', onDownloadProgress: (progressEvent) => { console.log(`Downloaded: ${progressEvent.loaded} bytes`) } })`. Works in browsers via XMLHttpRequest progress events.

## Q24: How do you set custom headers in Axios?
**A:** Pass headers in config: `axios.get('/api', { headers: { 'X-Custom': 'value', 'Authorization': 'Bearer token' } })`. For all requests, set defaults: `axios.defaults.headers.common['X-App-Version'] = '1.0'`.

## Q25: How do you send query parameters with Axios?
**A:** Use `params` in config: `axios.get('/api/users', { params: { page: 1, limit: 10, sort: '-createdAt' } })`. Axios serializes the params object into the URL query string. Arrays and nested objects are serialized automatically.

## Q26: How do you send request body data with Axios?
**A:** Pass as the second argument for POST/PUT/PATCH: `axios.post('/api/users', { name: 'John', age: 30 })`. Axios serializes objects to JSON and sets Content-Type: application/json automatically.

## Q27: How does Axios handle JSON data?
**A:** Axios automatically serializes JavaScript objects to JSON for request bodies and parses JSON response bodies. This is the default `transformRequest` and `transformResponse` behavior. Override with custom transformers if needed.

## Q28: How do you transform request data before sending?
**A:** Use `transformRequest`: `axios.post('/api', data, { transformRequest: [(data, headers) => { headers['Content-Type'] = 'text/xml'; return xmlConverter.toXML(data) }] })`. The function receives the request data and headers.

## Q29: How do you transform response data after receiving?
**A:** Use `transformResponse`: `axios.get('/api', { transformResponse: [axios.defaults.transformResponse[0], (data) => { return data.map(item => ({ ...item, fullName: `${item.first} ${item.last}` })) }] })`. Multiple transformers run in order.

## Q30: How do you handle SSL certificates in Axios (Node.js)?
**A:** Node.js options: `httpsAgent: new https.Agent({ rejectUnauthorized: false })` (not recommended for production). For custom CA: `httpsAgent: new https.Agent({ ca: fs.readFileSync('ca.pem') })`. In browsers, SSL is handled automatically.

## Q31: How do you use Axios with TypeScript?
**A:** Import types: `import axios, { AxiosResponse, AxiosError } from 'axios'`. Generic response typing: `axios.get<{ id: number, name: string }>('/api/users/1')`. Then `response.data` is typed. Also `AxiosRequestConfig` for request options.

## Q32: How do you type Axios response data?
**A:** Use generics: `interface User { id: number; name: string }; const res = await axios.get<User>('/api/users/1'); res.data.name // typed as string`. For arrays: `axios.get<User[]>('/api/users')`.

## Q33: How do you type Axios error responses?
**A:** Handle `AxiosError<T>` where T is the response error type: `catch (error: AxiosError<{ message: string }>) { if (error.response) { error.response.data.message } }`. Check `AxiosError` for type-safe error handling.

## Q34: What is `AxiosHeaders` in Axios v1+?
**A:** `AxiosHeaders` is a class providing a structured way to manage headers. Supports case-insensitive access, setting/getting headers, and serialization. Used internally but can be accessed: `const headers = new AxiosHeaders({ 'Content-Type': 'application/json' })`.

## Q35: How do you validate HTTP status codes in Axios?
**A:** By default, Axios rejects for any status outside 200-299. Customize with `validateStatus`: `axios.get('/api', { validateStatus: (status) => status < 500 })`. Return true for acceptable statuses.

## Q36: How do you handle network errors in Axios?
**A:** Network errors have `error.code === 'ERR_NETWORK'` (or `'ENETUNREACH'` in older versions). Check `error.message` for details. Network errors don't have an `error.response`. Handle gracefully with retry logic or user notification.

## Q37: How do you handle timeout errors in Axios?
**A:** Timeout errors have `error.code === 'ECONNABORTED'` and `error.message === 'timeout of Xms exceeded'`. Check `error.code` in the error handler. Implement retry with exponential backoff for transient timeouts.

## Q38: How do you implement request retry in Axios?
**A:** Use a response interceptor: track retry count in `config._retry`. On failure, if retries remain, wait and retry: `return new Promise(resolve => setTimeout(() => resolve(axios(config)), delay))`. Or use `axios-retry` library for automatic retry.

## Q39: How do you use `axios-retry`?
**A:** Install `axios-retry`. Configure: `import axiosRetry from 'axios-retry'; axiosRetry(axios, { retries: 3, retryDelay: axiosRetry.exponentialDelay, retryCondition: (error) => error.response?.status >= 500 })`. Adds automatic retry with configurable strategies.

## Q40: How do you use Axios with React Query / TanStack Query?
**A:** Use Axios as the fetch function: `useQuery({ queryKey: ['users'], queryFn: () => axios.get('/api/users').then(res => res.data) })`. TanStack Query handles caching, retries, and state management on top of Axios.

## Q41: How do you use Axios with Next.js server components?
**A:** Import `axios` in server components or server actions. Make requests to internal or external APIs. No special configuration needed. For external APIs, use `cache: 'no-store'` or appropriate fetch caching.

## Q42: How do you use Axios in React Native?
**A:** Same API as web Axios. No additional configuration needed for basic HTTP requests. For SSL pinning, use `react-native-ssl-pinning` with Axios. For base URL, use environment variables.

## Q43: How do you set a base URL in Axios?
**A:** `axios.defaults.baseURL = 'https://api.example.com/v2'`. Or per instance: `axios.create({ baseURL: 'https://api.example.com' })`. All relative URLs in requests are resolved against the base URL.

## Q44: How do you configure Axios for server-side rendering (SSR)?
**A:** Create a new Axios instance per request (to avoid token leakage). Pass cookies from the incoming request. Use baseURL pointing to the internal API. Handle API errors gracefully with fallback UI.

## Q45: How does Axios handle cookies?
**A:** In browsers, Axios sends cookies automatically for same-origin requests. For cross-origin, set `withCredentials: true`: `axios.get('https://api.other.com', { withCredentials: true })`. The server must allow credentials in CORS.

## Q46: How do you send cookies with cross-origin requests?
**A:** `axios.get('https://api.example.com', { withCredentials: true })`. Requires the server's CORS configuration to include `Access-Control-Allow-Credentials: true` and specific origin (not `*`).

## Q47: How do you handle CORS errors in Axios?
**A:** CORS errors are browser-enforced; Axios receives them as network errors. Fix by configuring the server with proper CORS headers (`Access-Control-Allow-Origin`, etc.). For development, use a proxy.

## Q48: How do you use Axios with a proxy?
**A:** In Node.js: `axios.get('/api', { proxy: { host: '127.0.0.1', port: 3000, protocol: 'http' } })`. In browsers, CORS proxy: use a proxy server URL as baseURL. For React dev, use the Vite/CRA proxy configuration.

## Q49: How do you use Axios in Node.js with HTTP/HTTPS agents?
**A:** `const https = require('https'); axios.get('/api', { httpsAgent: new https.Agent({ keepAlive: true }) })`. Custom agents control connection pooling, SSL config, and proxy settings. Use `http.Agent` for HTTP connections.

## Q50: How do you handle large responses with Axios?
**A:** For large JSON: use `transformResponse` to stream-parse. For binary data: `responseType: 'stream'` (Node.js) or `responseType: 'blob'` (browser). For large datasets, implement pagination to limit response size.

## Q51: How do you stream responses in Node.js with Axios?
**A:** `axios.get('/large-file', { responseType: 'stream' }).then(response => { response.data.pipe(fs.createWriteStream('output.txt')) })`. The `response.data` is a readable stream. Useful for downloading large files without buffering in memory.

## Q52: How do you stream requests in Node.js with Axios?
**A:** Pass a readable stream as the request body: `const stream = fs.createReadStream('input.txt'); axios.post('/upload', stream, { headers: { 'Content-Type': 'application/octet-stream' } })`. Axios pipes the stream to the request.

## Q53: How do you handle multipart form data with Axios?
**A:** Use `FormData`: `const form = new FormData(); form.append('field', 'value'); form.append('file', file); axios.post('/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })`. Axios auto-detects FormData and sets the correct content type.

## Q54: How do you use Axios with OAuth2?
**A:** Store access token, send in Authorization header: `axios.defaults.headers.common['Authorization'] = 'Bearer ' + token`. Handle token refresh in response interceptor on 401. For client credentials grant, request token on app startup.

## Q55: How do you test Axios requests?
**A:** Use `axios-mock-adapter` to mock responses: `const mock = new MockAdapter(axios); mock.onGet('/users').reply(200, [{ id: 1 }])`. Or use `msw` (Mock Service Worker) for more comprehensive request mocking.

## Q56: What is `axios-mock-adapter`?
**A:** A library for mocking Axios requests in tests. `mock.onGet('/api/users').reply(200, users)`. Supports reply chaining, network errors, timeouts, and conditional matching. Works by overriding the Axios adapter.

## Q57: How do you mock Axios in Jest?
**A:** Jest mock: `jest.mock('axios'); const mockedAxios = axios as jest.Mocked<typeof axios>; mockedAxios.get.mockResolvedValue({ data: users })`. Or use `axios-mock-adapter` for more realistic mocking.

## Q58: How do you handle concurrent requests with progress?
**A:** Use `axios.all` (legacy) or `Promise.all` with individual progress tracking. For complex progress, use a counter: `let completed = 0; const total = urls.length; urls.forEach(url => { axios.get(url).then(() => { completed++; console.log(`${completed/total*100}%`); }) })`.

## Q59: How do you batch requests with Axios?
**A:** Send multiple requests in parallel with `Promise.all()` or sequentially with async/await. For rate-limited APIs, use a queue that processes requests one at a time or in limited concurrency batches.

## Q60: How do you implement request queuing with Axios?
**A:** Create a queue class: push requests to an array, process them sequentially with a configurable concurrency limit. Use a response interceptor to handle rate limit (429) responses and requeue with delay.

## Q61: How do you handle 429 (Too Many Requests) in Axios?
**A:** In the response interceptor, check for status 429. Parse the `Retry-After` header for wait duration. Delay and retry: `const retryAfter = error.response.headers['retry-after']; await new Promise(r => setTimeout(r, retryAfter * 1000)); return axios(error.config)`.

## Q62: How do you implement exponential backoff in Axios?
**A:** In retry logic: `const delay = Math.pow(2, attempt) * 1000 + Math.random() * 1000`. Wait before retry: `await new Promise(r => setTimeout(r, delay))`. Random jitter prevents thundering herd on retry.

## Q63: How do you use Axios with WebSockets?
**A:** Axios does not support WebSockets directly. Use libraries like `socket.io-client` or `ws` for WebSocket connections. Axios is for HTTP/HTTPS requests only.

## Q64: How do you handle redirects in Axios?
**A:** In browsers, Axios follows redirects automatically (HTTP redirect). In Node.js, configure `maxRedirects`: `axios.get('/api', { maxRedirects: 5 })`. Set to 0 to disable redirect following. The final response is returned after all redirects.

## Q65: How do you disable redirects in Axios (Node.js)?
**A:** `axios.get('/api', { maxRedirects: 0 })`. Axios will not follow redirects, and the response with 3xx status is returned directly. Handle redirects manually if needed.

## Q66: How do you use Axios with HTTP/2?
**A:** Axios currently uses HTTP/1.1 by default. For HTTP/2 in Node.js, use a custom `http2` wrapper or libraries like `got` or `undici`. HTTP/2 support in Axios is limited.

## Q67: How do you use Axios with gzip compression?
**A:** In browsers, Axios handles gzip decompression automatically. In Node.js, Axios also handles it automatically for both request and response bodies.

## Q68: How do you handle binary data with Axios?
**A:** Set `responseType` appropriately: `'arraybuffer'` for binary data, `'blob'` for browser blobs, `'document'` for XML, `'stream'` for Node.js streams. Access with `response.data` after parsing.

## Q69: How do you download a file with Axios?
**A:** Browser: `axios.get('/file.pdf', { responseType: 'blob' }).then(res => { const url = URL.createObjectURL(res.data); const a = document.createElement('a'); a.href = url; a.download = 'file.pdf'; a.click() })`. Node.js: pipe to file write stream.

## Q70: How do you upload multiple files with Axios?
**A:** Append multiple files to FormData: `const form = new FormData(); files.forEach(file => form.append('files', file)); axios.post('/upload-multiple', form)`. The server receives an array of files.

## Q71: How do you use Axios with GraphQL?
**A:** POST request to GraphQL endpoint: `axios.post('/graphql', { query: `{ users { id name } }` })`. For Apollo Client, use `HttpLink` instead of Axios. Axios can be used for direct GraphQL queries without a client library.

## Q72: How do you use Axios with authentication tokens?
**A:** Set in request interceptor: `axios.interceptors.request.use(config => { config.headers.Authorization = `Bearer ${getToken()}`; return config })`. Or per request: `axios.get('/api', { headers: { Authorization: 'Bearer ' + token } })`.

## Q73: How do you handle token storage securely?
**A:** Store tokens in httpOnly cookies (not accessible to JS). For SPA: use in-memory storage with refresh tokens, not localStorage (XSS vulnerable). Use short-lived access tokens with refresh token rotation.

## Q74: How do you implement silent token refresh with Axios?
**A:** In response interceptor on 401: check if original request failed due to expired token. Lock the refresh (prevent concurrent refreshes). Call refresh endpoint, update token, retry all queued requests. Unlock after refresh completes.

## Q75: How do you use Axios with service workers?
**A:** Service workers intercept network requests. Axios requests go through the service worker automatically (browser). Configure cache-first or network-first strategies in the service worker for offline support.

## Q76: How do you use form-urlencoded data with Axios?
**A:** `axios.post('/api', 'field1=value1&field2=value2', { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })`. Or use `qs` library or `URLSearchParams` to serialize objects.

## Q77: How do you use URLSearchParams with Axios?
**A:** `const params = new URLSearchParams(); params.append('field', 'value'); axios.post('/api', params.toString(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })`. Axios does not automatically stringify URLSearchParams.

## Q78: What is the difference between Axios and Fetch API?
**A:** Fetch is native (no library needed). Axios provides: automatic JSON parsing, request/response interceptors, request cancellation (AbortController), progress events, timeout support, better error handling, older browser support, and a simpler API for common patterns.

## Q79: What are the advantages of Axios over Fetch?
**A:** (1) Automatic JSON transformation, (2) Request/response interceptors, (3) Request cancellation, (4) Progress events for upload/download, (5) Timeout handling, (6) Better error objects with response details, (7) Instance-based configuration, (8) Browser and Node.js support.

## Q80: What are the disadvantages of Axios?
**A:** (1) Extra bundle size (~14KB gzipped), (2) Another dependency to maintain, (3) Fetch is native and doesn't require installation, (4) Fetch has better streaming support (ReadableStream), (5) Fetch has better integration with service workers.

## Q81: How do you migrate from Fetch to Axios?
**A:** Replace `fetch(url, options)` with `axios(url, options)`. Change `.then(res => res.json())` to direct `res.data`. Replace error handling with `axios.isAxiosError(error)` checks. Add interceptors for global behavior.

## Q82: How do you use Axios with environment variables?
**A:** Store API URL in env var: `const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL })`. Use `.env.local` for local development. For Next.js, prefix with `NEXT_PUBLIC_` for client-side access.

## Q83: How do you handle non-JSON responses in Axios?
**A:** Axios tries to parse JSON by default. For non-JSON responses, set `responseType`: `'text'` for text, `'blob'` for binary, `'arraybuffer'` for buffers. Or use empty `transformResponse` to get raw string.

## Q84: How do you get raw response headers in Axios?
**A:** Access `response.headers` object. It's a plain object with header names as keys (lowercase). For raw header string, access `response.headers` raw property if available.

## Q85: How do you abort multiple requests with Axios?
**A:** Use `AbortController` for each request, or one controller for multiple requests: `const controller = new AbortController(); axios.get('/api/1', { signal: controller.signal }); axios.get('/api/2', { signal: controller.signal }); controller.abort()`.

## Q86: How do you use Axios with rate limiting on the client?
**A:** Implement a request queue that respects rate limits. Use a token bucket or sliding window algorithm. In the interceptor, delay requests when approaching limits. Parse `X-RateLimit-*` response headers to track usage.

## Q87: How do you create a type-safe API client with Axios?
**A:** Define request/response interfaces. Create typed methods: `const getUsers = (): Promise<User[]> => axios.get('/api/users').then(res => res.data)`. Use Axios generics: `axios.get<User[]>('/api/users')`.

## Q88: How do you handle offline state in Axios?
**A:** Detect offline with `navigator.onLine`. Queue failed requests in IndexedDB or in-memory. When back online, replay the queue. Use a response interceptor to detect network errors and queue them.

## Q89: How do you use Axios with caching?
**A:** Implement client-side caching: store responses in a Map or IndexedDB keyed by URL. In the request interceptor, check cache and return cached response. Or use `axios-cache-interceptor` library for advanced caching.

## Q90: How do you use Axios with TanStack Query for caching?
**A:** TanStack Query manages caching. Use Axios as the query function: `useQuery({ queryKey: ['users'], queryFn: () => axios.get('/api/users').then(r => r.data), staleTime: 5 * 60 * 1000 })`. TanStack handles cache invalidation and refetching.

## Q91: How do you implement deduplication of identical Axios requests?
**A:** In the request interceptor, check if there's an in-flight request with the same method+URL+data. If so, return that pending promise instead of creating a new request. Use a Map to track in-flight requests.

## Q92: How do you use Axios with monorepo shared API client?
**A:** Create a shared package with Axios instance, types, and API methods. Each app imports from the shared package. Configure baseURL per environment. Use different instances for different API versions.

## Q93: How do you handle CSRF tokens with Axios?
**A:** Read CSRF token from cookie (e.g., `XSRF-TOKEN`). Axios automatically sets `X-XSRF-TOKEN` header for same-origin requests if the cookie is present. Configure `xsrfCookieName` and `xsrfHeaderName` in Axios config.

## Q94: What is Axios XSRF protection?
**A:** Axios automatically includes an `X-XSRF-TOKEN` header (from the `XSRF-TOKEN` cookie) in every request. This helps protect against CSRF attacks. Configure with `xsrfCookieName` and `xsrfHeaderName` options.

## Q95: How do you disable XSRF protection in Axios?
**A:** Set `xsrfCookieName: null` or set the relevant options to empty strings. Not recommended unless you have an alternative CSRF protection mechanism.

## Q96: How do you use Axios with server-sent events (SSE)?
**A:** Axios is not ideal for SSE. Use the native `EventSource` API or a dedicated SSE library. Axios can make the initial request but doesn't handle persistent streaming connections well.

## Q97: How do you handle HTTP/2 server push with Axios?
**A:** Axios doesn't support HTTP/2 server push. HTTP/2 push is handled at the protocol level by the browser. For Node.js, consider using HTTP/2 compatible libraries.

## Q98: How do you use Axios in Electron apps?
**A:** Same as browser usage. Axios works in Electron's renderer process. For main process requests, use Axios or Node.js `http` module. Consider using `net` module for performance (Chromium's networking stack).

## Q99: What are Axios cancellation tokens (legacy)?
**A:** Pre-v0.22 cancellation used `CancelToken.source()`: `const source = axios.CancelToken.source(); axios.get('/api', { cancelToken: source.token }); source.cancel('Cancelled')`. Deprecated in favor of AbortController.

## Q100: What are the best practices for Axios?
**A:** (1) Create instances with baseURL, (2) Use interceptors for auth and error handling, (3) Implement token refresh in interceptors, (4) Use TypeScript generics for type safety, (5) Set timeouts, (6) Handle errors gracefully with status code checks, (7) Use AbortController for cancellation, (8) Implement retry with exponential backoff, (9) Test with axios-mock-adapter, (10) Keep sensitive data out of request config (logs, errors).
