# TypeScript + WebAssembly Integration

## Table of Contents

1. [WebAssembly Fundamentals](#webassembly-fundamentals)
2. [AssemblyScript](#assemblyscript)
3. [WASM Module Typing](#wasm-module-typing)
4. [WebAssembly.instantiate Types](#webassemblyinstantiate-types)
5. [WASM Imports/Exports Typing](#wasm-importsexports-typing)
6. [wasm-pack and wasm-bindgen](#wasm-pack-and-wasm-bindgen)
7. [Practical Patterns](#practical-patterns)
8. [Interview Questions](#interview-questions)

---

## WebAssembly Fundamentals

```typescript
// WebAssembly (WASM) is a binary instruction format that runs
// at near-native speed in the browser and Node.js.
//
// TypeScript interacts with WASM through the WebAssembly API.
// WASM modules communicate with JS through typed imports/exports.

// A WASM module is compiled from a source language (Rust, C, Go,
// AssemblyScript) into .wasm binary files. These modules can:
// - Export functions callable from JavaScript
// - Import functions provided by JavaScript
// - Share memory (WebAssembly.Memory) with JavaScript
// - Process data at near-native speed

// Basic WASM loading and execution in TypeScript:
async function loadWasmModule(): Promise<WebAssembly.Exports> {
  const response = await fetch('./module.wasm');
  const bytes = await response.arrayBuffer();
  const { instance } = await WebAssembly.instantiate(bytes);
  return instance.exports;
}

// The WebAssembly namespace provides:
// - WebAssembly.Module: Compiled WASM module
// - WebAssembly.Instance: Instantiated module with state
// - WebAssembly.Memory: Shared linear memory
// - WebAssembly.Table: Function reference table
// - WebAssembly.instantiate: Compile and instantiate
// - WebAssembly.compile: Compile without instantiating
```

---

## AssemblyScript

```typescript
// AssemblyScript is a TypeScript-like language that compiles to WASM.
// It uses a strict subset of TypeScript syntax with WASM-specific types.

// assembly/index.ts — AssemblyScript code
// export function add(a: i32, b: i32): i32 {
//   return a + b;
// }
//
// export function fibonacci(n: i32): i32 {
//   if (n <= 1) return n;
//   let a: i32 = 0;
//   let b: i32 = 1;
//   for (let i: i32 = 2; i <= n; i++) {
//     const temp = a + b;
//     a = b;
//     b = temp;
//   }
//   return b;
// }
//
// export function factorial(n: i64): i64 {
//   if (n <= 1) return 1;
//   return n * factorial(n - 1);
// }

// TypeScript types for AssemblyScript WASM modules:
interface AssemblyScriptModule extends WebAssembly.Module {
  // AssemblyScript exports are typed as WASM value types
}

// Typing the WASM exports after instantiation:
interface WASMExports {
  add(a: number, b: number): number;
  fibonacci(n: number): number;
  factorial(n: number): number;
}

// Memory management — AssemblyScript manages its own memory
interface ASMemory {
  memory: WebAssembly.Memory;
  // AssemblyScript-specific memory helpers
}

// Loading and using an AssemblyScript module:
async function useAssemblyScript(): Promise<WASMExports> {
  const response = await fetch('./assembly/index.wasm');
  const { instance } = await WebAssembly.instantiateStreaming(response);

  const exports = instance.exports as WASMExports;

  // Fully typed calls to WASM functions
  const sum = exports.add(2, 3);      // sum = 5
  const fib = exports.fibonacci(10);  // fib = 55
  const fact = exports.factorial(20); // fact = 2432902008176640000

  return exports;
}

// asconfig.json — AssemblyScript compiler configuration
const asConfig = {
  "entry": "assembly/index.ts",
  "out": "build/optimized.wasm",
  "textFile": "build/optimized.wat",
  "target": "release",
  "options": {
    "runtime": "minimal",
    "unchecked": false,
    "exportRuntime": false
  }
};
```

---

## WASM Module Typing

```typescript
// Creating comprehensive type definitions for WASM modules:

// 1. Define the expected exports
interface ImageProcessorExports {
  grayscale(buffer: number, width: number, height: number): void;
  blur(buffer: number, width: number, height: number, radius: number): void;
  resize(
    buffer: number,
    width: number,
    height: number,
    newWidth: number,
    newHeight: number
  ): number; // returns pointer to new buffer
  free(ptr: number, size: number): void;
}

// 2. Define the expected imports
interface ImageProcessorImports {
  env: {
    memory: WebAssembly.Memory;
    abort(message: number, filename: number, line: number, column: number): void;
    consoleLog(ptr: number, len: number): void;
  };
}

// 3. Define the complete module interface
interface ImageProcessorModule {
  instance: WebAssembly.Instance;
  exports: ImageProcessorExports;
  memory: WebAssembly.Memory;
}

// 4. Type-safe WASM loader
async function loadImageProcessor(): Promise<ImageProcessorModule> {
  const memory = new WebAssembly.Memory({
    initial: 256,  // 256 pages = 16MB
    maximum: 1024, // 1024 pages = 64MB
  });

  const imports: ImageProcessorImports = {
    env: {
      memory,
      abort: (message, filename, line, column) => {
        throw new Error(`WASM abort at ${line}:${column}`);
      },
      consoleLog: (ptr, len) => {
        const bytes = new Uint8Array(memory.buffer, ptr, len);
        const text = new TextDecoder().decode(bytes);
        console.log(text);
      },
    },
  };

  const response = await fetch('./image-processor.wasm');
  const { instance } = await WebAssembly.instantiateStreaming(response, imports);

  return {
    instance,
    exports: instance.exports as unknown as ImageProcessorExports,
    memory,
  };
}

// 5. Type-safe wrapper around raw WASM calls
class ImageProcessor {
  private exports: ImageProcessorExports;
  private memory: WebAssembly.Memory;
  private heap: Uint8Array;

  constructor(module: ImageProcessorModule) {
    this.exports = module.exports;
    this.memory = module.memory;
    this.heap = new Uint8Array(module.memory.buffer);
  }

  // Copy image data into WASM memory
  private writeToMemory(data: Uint8Array): number {
    const ptr = this.malloc(data.length);
    this.heap.set(data, ptr);
    return ptr;
  }

  // Read image data from WASM memory
  private readFromMemory(ptr: number, length: number): Uint8Array {
    return new Uint8Array(this.memory.buffer, ptr, length);
  }

  private malloc(size: number): number {
    // In real usage, implement a proper allocator or use WASM's memory.grow
    return this.exports.resize(0, 0, 0, size, 0);
  }

  grayscale(imageData: Uint8Array): Uint8Array {
    const ptr = this.writeToMemory(imageData);
    this.exports.grayscale(ptr, 0, 0);
    const result = this.readFromMemory(ptr, imageData.length);
    this.exports.free(ptr, imageData.length);
    return new Uint8Array(result);
  }
}

// .d.ts file for pre-compiled WASM modules
// types/image-processor.d.ts
declare module 'image-processor.wasm' {
  const module: WebAssembly.Module;
  export default module;
}

// Or declare the WASM as a module with typed exports:
declare module '*/image-processor.wasm' {
  export interface Exports {
    grayscale(buffer: number, width: number, height: number): void;
    blur(buffer: number, width: number, height: number, radius: number): void;
    resize(
      buffer: number,
      width: number,
      height: number,
      newWidth: number,
      newHeight: number
    ): number;
    free(ptr: number, size: number): void;
  }

  const wasm: WebAssembly.Module;
  export default wasm;
}
```

---

## WebAssembly.instantiate Types

```typescript
// The WebAssembly.instantiate function has multiple overloads:

// Overload 1: Streaming instantiation (most common)
async function streamingInstantiate(
  source: Response | Promise<Response>,
  imports?: WebAssembly.Imports
): Promise<WebAssembly.WebAssemblyInstantiatedSource>;

// Overload 2: ArrayBuffer instantiation
async function arrayBufferInstantiate(
  bufferSource: BufferSource,
  imports?: WebAssembly.Imports
): Promise<WebAssembly.WebAssemblyInstantiatedSource>;

// Overload 3: Module instantiation (already compiled)
function moduleInstantiate(
  module: WebAssembly.Module,
  imports?: WebAssembly.Imports
): WebAssembly.Instance;

// Type definitions from lib.dom.d.ts:
namespace WebAssembly {
  interface WebAssemblyInstantiatedSource {
    module: Module;
    instance: Instance;
  }

  interface Module {
    /** Returns a list of the names of the module's exports. */
    readonly exports: ExportedModuleExport[];

    /** Returns a list of the module's imports. */
    readonly imports: ImportedModuleImport[];
  }

  interface Instance {
    readonly exports: Exports;
  }

  type Exports = Record<string, Function>;

  interface Imports {
    [module: string]: Record<string, Function>;
  }

  interface MemoryDescriptor {
    initial?: number;
    maximum?: number;
    shared?: boolean;
  }

  class Memory {
    readonly buffer: ArrayBuffer;
    constructor(descriptor?: MemoryDescriptor);
    grow(delta: number): number;
  }

  class Table {
    readonly length: number;
    constructor(descriptor?: TableDescriptor);
    get(index: number): Function;
    grow(delta: number): number;
    set(index: number, value: Function): void;
  }
}

// Practical usage with proper typing:
async function loadTypedWasm<T extends WebAssembly.Exports>(
  url: string,
  imports?: WebAssembly.Imports
): Promise<T> {
  const response = await fetch(url);
  const { instance } = await WebAssembly.instantiateStreaming(response, imports);
  return instance.exports as T;
}

// Usage:
interface MathExports {
  sin(x: number): number;
  cos(x: number): number;
  sqrt(x: number): number;
  fastFourierTransform(input: number, output: number, n: number): void;
}

const math = await loadTypedWasm<MathExports>('./math.wasm');
const sinValue = math.sin(Math.PI / 4); // fully typed
```

---

## WASM Imports/Exports Typing

```typescript
// Typing the full contract between JS and WASM:

// ============= JavaScript -> WASM Imports =============
interface CryptoWASMImports {
  env: {
    memory: WebAssembly.Memory;
  };
  // WASM imports a JS function for random bytes
  js: {
    randomBytes(ptr: number, length: number): void;
    currentTime(): number;
    logMessage(ptr: number, length: number): void;
  };
}

// ============= WASM -> JS Exports =============
interface CryptoWASMExports {
  // Exported WASM functions
  sha256(inputPtr: number, inputLen: number, outputPtr: number): void;
  aesEncrypt(
    dataPtr: number,
    dataLen: number,
    keyPtr: number,
    keyLen: number,
    outputPtr: number
  ): number; // returns output length
  aesDecrypt(
    dataPtr: number,
    dataLen: number,
    keyPtr: number,
    keyLen: number,
    outputPtr: number
  ): number;
  free(ptr: number, size: number): void;
}

// ============= Type-safe WASM wrapper =============
class WASMCrypto {
  private memory: WebAssembly.Memory;
  private exports: CryptoWASMExports;
  private heap: Uint8Array;

  constructor(exports: CryptoWASMExports, memory: WebAssembly.Memory) {
    this.exports = exports;
    this.memory = memory;
    this.heap = new Uint8Array(memory.buffer);
  }

  private alloc(size: number): number {
    // Simple bump allocator for WASM memory
    const currentSize = this.heap.length;
    if (currentSize + size > this.memory.buffer.byteLength) {
      const pagesNeeded = Math.ceil((currentSize + size - this.memory.buffer.byteLength) / 65536);
      this.memory.grow(pagesNeeded);
      this.heap = new Uint8Array(this.memory.buffer);
    }
    const ptr = currentSize;
    return ptr;
  }

  private writeBytes(data: Uint8Array): number {
    const ptr = this.alloc(data.length);
    this.heap.set(data, ptr);
    return ptr;
  }

  private readBytes(ptr: number, length: number): Uint8Array {
    return new Uint8Array(this.memory.buffer, ptr, length).slice();
  }

  sha256(data: Uint8Array): Uint8Array {
    const inputPtr = this.writeBytes(data);
    const outputPtr = this.alloc(32); // SHA-256 = 32 bytes
    this.exports.sha256(inputPtr, data.length, outputPtr);
    const hash = this.readBytes(outputPtr, 32);
    this.exports.free(inputPtr, data.length);
    return hash;
  }

  aesEncrypt(data: Uint8Array, key: Uint8Array): Uint8Array {
    const dataPtr = this.writeBytes(data);
    const keyPtr = this.writeBytes(key);
    const outputPtr = this.alloc(data.length + 16); // padding
    const outputLen = this.exports.aesEncrypt(
      dataPtr, data.length,
      keyPtr, key.length,
      outputPtr
    );
    const encrypted = this.readBytes(outputPtr, outputLen);
    this.exports.free(dataPtr, data.length);
    this.exports.free(keyPtr, key.length);
    return encrypted;
  }
}

// ============= Instantiation with typed imports =============
async function initWASM(): Promise<WASMCrypto> {
  const memory = new WebAssembly.Memory({ initial: 256, maximum: 1024 });

  const imports: CryptoWASMImports = {
    env: { memory },
    js: {
      randomBytes: (ptr: number, length: number) => {
        const bytes = crypto.getRandomValues(new Uint8Array(length));
        new Uint8Array(memory.buffer, ptr, length).set(bytes);
      },
      currentTime: () => Date.now(),
      logMessage: (ptr: number, length: number) => {
        const msg = new TextDecoder().decode(
          new Uint8Array(memory.buffer, ptr, length)
        );
        console.log('[WASM]', msg);
      },
    },
  };

  const response = await fetch('./crypto.wasm');
  const { instance } = await WebAssembly.instantiateStreaming(response, imports);

  return new WASMCrypto(
    instance.exports as unknown as CryptoWASMExports,
    memory
  );
}

const crypto = await initWASM();
const hash = crypto.sha256(new TextEncoder().encode('hello world'));
console.log(Array.from(hash).map(b => b.toString(16).padStart(2, '0')).join(''));
```

---

## wasm-pack and wasm-bindgen

```typescript
// wasm-bindgen (Rust) and wasm-pack generate TypeScript bindings
// automatically. The generated .d.ts files provide full type safety.

// Rust source (lib.rs):
// use wasm_bindgen::prelude::*;
//
// #[wasm_bindgen]
// pub fn greet(name: &str) -> String {
//     format!("Hello, {}!", name)
// }
//
// #[wasm_bindgen]
// pub struct Calculator {
//     value: f64,
// }
//
// #[wasm_bindgen]
// impl Calculator {
//     #[wasm_bindgen(constructor)]
//     pub fn new(initial: f64) -> Calculator {
//         Calculator { value: initial }
//     }
//
//     pub fn add(&mut self, n: f64) {
//         self.value += n;
//     }
//
//     pub fn get_value(&self) -> f64 {
//         self.value
//     }
// }

// Generated TypeScript bindings (pkg/my_wasm.d.ts):
// /* tslint:disable */
// /* eslint-disable */
// export function greet(name: string): string;
// export class Calculator {
//   free(): void;
//   constructor(initial: number);
//   add(n: number): void;
//   get_value(): number;
// }

// Using the generated bindings in TypeScript:
import init, { greet, Calculator } from './pkg/my_wasm';

async function main(): Promise<void> {
  // Initialize the WASM module (required before calling any functions)
  await init();

  // Fully typed function call
  const greeting: string = greet('TypeScript');
  console.log(greeting); // "Hello, TypeScript!"

  // Typed class usage
  const calc = new Calculator(0);
  calc.add(5);
  calc.add(3);
  const value: number = calc.get_value();
  console.log(value); // 8
  calc.free(); // Explicit memory cleanup
}

// wasm-bindgen generates these type mappings:
// Rust type        -> TypeScript type
// i8, i16, i32     -> number
// u8, u16, u32     -> number
// i64, u64         -> bigint
// f32, f64         -> number
// bool             -> boolean
// String, &str     -> string
// Vec<T>           -> T[] (or Uint8Array for Vec<u8>)
// Option<T>        -> T | undefined
// Result<T, E>     -> T (throws on Err)
// JsValue          -> any
// &JsValue         -> any

// Advanced: typed struct with optional fields
// Rust:
// #[wasm_bindgen]
// pub struct Config {
//     pub width: u32,
//     pub height: u32,
//     pub format: String,
//     pub quality: Option<f64>,
// }
//
// #[wasm_bindgen]
// impl Config {
//     #[wasm_bindgen(constructor)]
//     pub fn new(width: u32, height: u32, format: &str) -> Config { ... }
// }

// Generated TypeScript:
// export class Config {
//   free(): void;
//   constructor(width: number, height: number, format: string);
//   width: number;
//   height: number;
//   format: string;
//   quality: number | undefined;
// }

// Full type safety with wasm-bindgen:
const config = new Config(1920, 1080, 'png');
config.quality = 0.95; // TypeScript validates the property exists
// config.nonexistent = true; // Error: property doesn't exist
```

---

## Practical Patterns

### Image Processing

```typescript
// A complete image processing pipeline using WASM for CPU-intensive operations:

interface ImageData {
  width: number;
  height: number;
  data: Uint8ClampedArray;
}

interface WasmImageExports {
  applyGrayscale(ptr: number, len: number): void;
  applySepia(ptr: number, len: number): void;
  applyEdgeDetection(ptr: number, len: number): void;
  applyBrightness(ptr: number, len: number, factor: number): void;
  applyContrast(ptr: number, len: number, factor: number): void;
  free(ptr: number, len: number): void;
}

class ImageProcessor {
  private memory: WebAssembly.Memory;
  private exports: WasmImageExports;

  constructor(exports: WasmImageExports, memory: WebAssembly.Memory) {
    this.exports = exports;
    this.memory = memory;
  }

  private writeToWasm(data: Uint8ClampedArray): number {
    const buffer = new Uint8Array(this.memory.buffer);
    // Grow memory if needed
    const needed = buffer.length + data.byteLength;
    if (needed > this.memory.buffer.byteLength) {
      this.memory.grow(Math.ceil(needed / 65536) + 1);
    }
    const ptr = buffer.length;
    buffer.set(new Uint8Array(data.buffer, data.byteOffset, data.byteLength), ptr);
    return ptr;
  }

  applyGrayscale(image: ImageData): ImageData {
    const totalLen = image.width * image.height * 4;
    const ptr = this.writeToWasm(image.data);

    this.exports.applyGrayscale(ptr, totalLen);

    const result = new Uint8ClampedArray(
      this.memory.buffer.slice(ptr, ptr + totalLen)
    );
    this.exports.free(ptr, totalLen);

    return { ...image, data: result };
  }

  applySepia(image: ImageData): ImageData {
    const totalLen = image.width * image.height * 4;
    const ptr = this.writeToWasm(image.data);

    this.exports.applySepia(ptr, totalLen);

    const result = new Uint8ClampedArray(
      this.memory.buffer.slice(ptr, ptr + totalLen)
    );
    this.exports.free(ptr, totalLen);

    return { ...image, data: result };
  }

  applyBrightness(image: ImageData, factor: number): ImageData {
    const totalLen = image.width * image.height * 4;
    const ptr = this.writeToWasm(image.data);

    this.exports.applyBrightness(ptr, totalLen, factor);

    const result = new Uint8ClampedArray(
      this.memory.buffer.slice(ptr, ptr + totalLen)
    );
    this.exports.free(ptr, totalLen);

    return { ...image, data: result };
  }

  // Chain multiple operations
  processPipeline(
    image: ImageData,
    operations: Array<{ type: string; params?: Record<string, number> }>
  ): ImageData {
    return operations.reduce((img, op) => {
      switch (op.type) {
        case 'grayscale': return this.applyGrayscale(img);
        case 'sepia': return this.applySepia(img);
        case 'brightness': return this.applyBrightness(img, op.params?.factor ?? 1.0);
        default: return img;
      }
    }, image);
  }
}

// Usage with Canvas API:
async function processImageInWasm(canvas: HTMLCanvasElement): Promise<void> {
  const ctx = canvas.getContext('2d')!;
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

  const memory = new WebAssembly.Memory({ initial: 1024 });
  const response = await fetch('./image-filters.wasm');
  const { instance } = await WebAssembly.instantiateStreaming(response, {
    env: { memory },
  });

  const processor = new ImageProcessor(
    instance.exports as unknown as WasmImageExports,
    memory
  );

  // Process with WASM — much faster than JS for pixel manipulation
  const processed = processor.processPipeline(imageData, [
    { type: 'grayscale' },
    { type: 'brightness', params: { factor: 1.2 } },
  ]);

  ctx.putImageData(processed, 0, 0);
}
```

### Cryptography

```typescript
// WASM for performant cryptographic operations:

interface CryptoWasmExports {
  sha256(ptr: number, len: number): number;
  sha512(ptr: number, len: number): number;
  pbkdf2(
    passwordPtr: number, passwordLen: number,
    saltPtr: number, saltLen: number,
    iterations: number,
    keyLen: number,
    outputPtr: number
  ): number;
  argon2Hash(
    passwordPtr: number, passwordLen: number,
    saltPtr: number, saltLen: number,
    timeCost: number,
    memoryCost: number,
    parallelism: number,
    outputLen: number,
    outputPtr: number
  ): number;
  free(ptr: number, size: number): void;
}

class WASMCryptoLib {
  private memory: WebAssembly.Memory;
  private exports: CryptoWasmExports;
  private heap: Uint8Array;
  private offset = 0;

  constructor(exports: CryptoWasmExports, memory: WebAssembly.Memory) {
    this.exports = exports;
    this.memory = memory;
    this.heap = new Uint8Array(memory.buffer);
  }

  private alloc(size: number): number {
    if (this.offset + size > this.heap.length) {
      this.memory.grow(Math.ceil((this.offset + size - this.heap.length) / 65536) + 1);
      this.heap = new Uint8Array(this.memory.buffer);
    }
    const ptr = this.offset;
    this.offset += size;
    return ptr;
  }

  private write(data: Uint8Array): number {
    const ptr = this.alloc(data.length);
    this.heap.set(data, ptr);
    return ptr;
  }

  private read(ptr: number, len: number): Uint8Array {
    return new Uint8Array(this.memory.buffer, ptr, len).slice();
  }

  sha256(data: Uint8Array): string {
    const ptr = this.write(data);
    const hashPtr = this.exports.sha256(ptr, data.length);
    const hash = this.read(hashPtr, 32);
    this.exports.free(hashPtr, 32);
    this.exports.free(ptr, data.length);
    return Array.from(hash).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  async pbkdf2(
    password: string,
    salt: string,
    iterations: number = 100000,
    keyLen: number = 32
  ): Promise<string> {
    const passwordBytes = new TextEncoder().encode(password);
    const saltBytes = new TextEncoder().encode(salt);

    const passwordPtr = this.write(passwordBytes);
    const saltPtr = this.write(saltBytes);
    const outputPtr = this.alloc(keyLen);

    this.exports.pbkdf2(
      passwordPtr, passwordBytes.length,
      saltPtr, saltBytes.length,
      iterations,
      keyLen,
      outputPtr
    );

    const key = this.read(outputPtr, keyLen);
    this.exports.free(passwordPtr, passwordBytes.length);
    this.exports.free(saltPtr, saltBytes.length);
    this.exports.free(outputPtr, keyLen);

    return Array.from(key).map(b => b.toString(16).padStart(2, '0')).join('');
  }
}

// Benchmark comparison
async function benchmarkCrypto(): Promise<void> {
  const data = new TextEncoder().encode('x'.repeat(1024 * 1024)); // 1MB

  // JS implementation
  const jsStart = performance.now();
  const jsHash = await crypto.subtle.digest('SHA-256', data);
  const jsTime = performance.now() - jsStart;

  // WASM implementation (would need actual WASM module)
  // const wasmStart = performance.now();
  // const wasmHash = wasmLib.sha256(data);
  // const wasmTime = performance.now() - wasmStart;

  console.log(`JS SHA-256: ${jsTime.toFixed(2)}ms`);
  // Typical result: JS ~15ms, WASM ~3-5ms for 1MB
  // For PBKDF2 with 100k iterations: JS ~500ms, WASM ~100ms
}
```

### Real-time Data Processing

```typescript
// WASM for real-time audio/video processing:

interface AudioProcessorExports {
  fft(inputPtr: number, outputPtr: number, n: number): void;
  lowPassFilter(
    inputPtr: number,
    outputPtr: number,
    length: number,
    cutoffFreq: number,
    sampleRate: number
  ): void;
  normalize(inputPtr: number, length: number): void;
  free(ptr: number, size: number): void;
}

class AudioAnalyzer {
  private memory: WebAssembly.Memory;
  private exports: AudioProcessorExports;

  constructor(exports: AudioProcessorExports, memory: WebAssembly.Memory) {
    this.exports = exports;
    this.memory = memory;
  }

  analyzeFrequency(
    audioSamples: Float32Array,
    sampleRate: number
  ): Float32Array {
    const n = audioSamples.length;
    const inputBytes = n * 4; // 4 bytes per float32
    const outputBytes = n * 4;

    const inputPtr = inputBytes;
    const outputPtr = inputBytes + outputBytes;

    // Write input to WASM memory
    new Float32Array(this.memory.buffer, inputPtr, n).set(audioSamples);

    // Run FFT in WASM (much faster than JS for large arrays)
    this.exports.fft(inputPtr, outputPtr, n);

    // Read result
    const result = new Float32Array(this.memory.buffer, outputPtr, n).slice();
    this.exports.free(inputPtr, inputBytes + outputBytes);
    return result;
  }

  // Real-time processing in AudioWorklet
  processFrame(samples: Float32Array): Float32Array {
    // WASM runs synchronously and fast enough for real-time audio
    this.exports.normalize(samplesPtr, samples.length);
    return samples;
  }
}

// Integration with AudioWorklet
class WASMAudioProcessor extends AudioWorkletProcessor {
  private wasmExports!: AudioProcessorExports;
  private memory!: WebAssembly.Memory;

  async init(): Promise<void> {
    const response = await fetch('./audio-filters.wasm');
    const { instance } = await WebAssembly.instantiate(response);
    this.memory = (instance.exports as any).memory;
    this.wasmExports = instance.exports as unknown as AudioProcessorExports;
  }

  process(inputs: Float32Array[][], outputs: Float32Array[][]): boolean {
    const input = inputs[0]?.[0];
    const output = outputs[0]?.[0];
    if (!input || !output) return true;

    // Copy input to WASM memory
    const inputPtr = 0;
    const outputPtr = input.length * 4;
    new Float32Array(this.memory.buffer, inputPtr, input.length).set(input);

    // Apply filter in WASM
    this.wasmExports.lowPassFilter(
      inputPtr, outputPtr, input.length, 1000, sampleRate
    );

    // Copy output back
    output.set(new Float32Array(this.memory.buffer, outputPtr, input.length));
    return true;
  }
}
```

---

## Interview Questions

### Q1: When should you use WebAssembly instead of pure TypeScript?

**Answer:** Use WASM for CPU-intensive, computation-heavy tasks: image/video processing, cryptography, physics simulations, data compression, and real-time audio processing. WASM provides near-native speed for these operations. For I/O-bound, DOM manipulation, or business logic, pure TypeScript is simpler and sufficient. WASM adds complexity (memory management, serialization overhead) that only pays off for compute-bound workloads.

### Q2: How does data pass between JavaScript and WASM?

**Answer:** Data passes through WASM's linear memory (a shared ArrayBuffer). JS writes data to a specific offset in memory, WASM reads from that offset, processes it, and writes results back. For simple types (numbers, booleans), direct passing works. For complex types (strings, arrays), you must serialize to bytes, pass the pointer and length, and deserialize on the other side. wasm-bindgen automates this for Rust.

### Q3: What is AssemblyScript and how does it differ from TypeScript?

**Answer:** AssemblyScript is a strict TypeScript subset that compiles directly to WASM. It uses WASM-specific types (i32, i64, f32, f64) instead of TypeScript's `number`. It has no `any`, no dynamic dispatch, and strict memory management. It's NOT TypeScript — it's a separate language with TypeScript-like syntax that targets WASM instead of JS.

### Q4: Explain the memory management model in WASM from TypeScript.

**Answer:** WASM uses a linear memory (ArrayBuffer) that grows in 64KB pages. JS and WASM share this memory. There's no garbage collector in WASM — you must manage allocation and deallocation manually (or use a WASM runtime's allocator). Common patterns: bump allocator for one-shot data, arena allocator for batch operations, explicit malloc/free. Memory.grow() expands the buffer, invalidating existing ArrayBuffer views.

### Q5: How do you type WASM imports and exports in TypeScript?

**Answer:** Define interfaces for the expected exports and imports. After instantiation, cast `instance.exports` to the typed interface. For imports, create a typed object matching the WASM module's import expectations. Example: `const exports = instance.exports as unknown as MyWasmExports;`. For wasm-bindgen, .d.ts files are auto-generated with full type information.

### Q6: What is wasm-bindgen and what does it provide?

**Answer:** wasm-bindgen is a Rust library that generates JavaScript bindings for Rust-compiled WASM modules. It handles: type conversion (Rust String <-> JS string), class generation (Rust struct -> JS class), memory management (automatic string/array passing), and TypeScript declaration file generation. wasm-pack is the build tool that uses wasm-bindgen under the hood.

### Q7: How would you debug WASM code from TypeScript?

**Answer:** Use Chrome DevTools — WASM debugging is supported since Chrome 70. Enable DWARF debugging info in the WASM build (emscripten: `-g`, Rust: `debug = true` in Cargo.toml). DevTools shows source-mapped Rust/C source alongside WASM disassembly. For logging, use WASM imports that call console.log. The `--generateTrace` equivalent for WASM is source maps + DWARF.
