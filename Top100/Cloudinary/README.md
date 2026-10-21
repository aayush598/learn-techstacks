# Cloudinary Interview Questions and Answers

## Q1: What is Cloudinary?
**A:** Cloudinary is a cloud-based media management platform that provides a comprehensive solution for uploading, storing, managing, manipulating, and delivering images and videos for web and mobile applications. It offers URL-based transformations, automatic optimization, CDN delivery, and AI-powered media analysis.

## Q2: What are the key features of Cloudinary?
**A:** (1) Image and video upload with automatic backups. (2) URL-based transformations (resize, crop, rotate, effects, filters). (3) Automatic optimization and responsive images. (4) AI-powered features (object recognition, auto-tagging, background removal). (5) Global CDN delivery. (6) DAM (Digital Asset Management) interface. (7) SDKs for major languages and frameworks.

## Q3: How does Cloudinary work?
**A:** Developers upload media assets to Cloudinary via API, SDK, or admin console. Cloudinary stores the asset, generates a unique public ID, and serves it via a CDN URL. Developers apply transformations by adding parameters to the URL. Cloudinary processes transformations on-the-fly and caches the results.

## Q4: What is a Cloudinary URL structure?
**A:** The URL format is: `https://res.cloudinary.com/<cloud_name>/<resource_type>/<type>/<transformations>/<version>/<public_id>.<extension>`. Example: `https://res.cloudinary.com/demo/image/upload/c_fill,w_300,h_300/v1/samples/landscape.jpg`

## Q5: What is a cloud name in Cloudinary?
**A:** A cloud name is your unique Cloudinary account identifier. It is a mandatory part of every Cloudinary URL. It is assigned when you sign up and appears in all media URLs. Example: `demo` in `res.cloudinary.com/demo/...`.

## Q6: What is a public ID in Cloudinary?
**A:** A public ID is a unique identifier for an asset in your Cloudinary account. It is assigned during upload (or auto-generated) and used in URLs to reference the asset. It can include folders: `products/shoe123`. Unlike filenames, public IDs are immutable once set.

## Q7: What are Cloudinary transformations?
**A:** Transformations are URL-based parameters that modify images and videos on-the-fly. They include resizing, cropping, rotation, effects, overlays, format conversion, quality adjustment, and more. Transformations are applied dynamically and cached for future requests.

## Q8: What is the difference between `c_fill`, `c_fit`, `c_scale`, and `c_crop` in Cloudinary?
**A:** `c_fill`: Resizes to fill given dimensions, cropping any excess (maintains aspect ratio). `c_fit`: Resizes to fit within dimensions (no cropping, may leave empty space). `c_scale`: Exactly scales to dimensions (ignores aspect ratio). `c_crop`: Extracts exact pixel region from the center without resizing.

## Q9: What is `c_pad` in Cloudinary?
**A:** `c_pad` resizes the image to fit within the given dimensions and adds padding (colored or transparent) to fill remaining space. It maintains aspect ratio. Use `b_<color>` to set padding color. Useful for creating uniform-sized thumbnails.

## Q10: What is `c_thumb` in Cloudinary?
**A:** `c_thumb` generates a thumbnail by focusing on a region of interest. It can crop to specific gravity (e.g., `g_face` for face detection, `g_auto` for automatic focus). It prioritizes the most important part of the image rather than the center.

## Q11: What is Cloudinary gravity?
**A:** Gravity determines which part of an image to focus on during cropping. Values include: `center` (default), `north`, `south`, `east`, `west`, `face` (detect and focus on faces), `faces` (all faces), `auto` (AI-based focus), `custom` (specify x/y coordinates), `soccer`, `subject`.

## Q12: What is `g_face` and `g_auto` in Cloudinary?
**A:** `g_face` uses face detection to focus on detected faces during cropping — ensures faces are centered. `g_auto` uses Cloudinary's AI to identify the most important region of the image (faces, objects, text) and crops accordingly. Both are gravity values.

## Q13: What are Cloudinary image optimization features?
**A:** (1) Automatic quality: `q_auto` — adjusts compression quality based on content. (2) Automatic format: `f_auto` — serves WebP/AVIF to compatible browsers. (3) Responsive breakpoints: auto-generates sizes. (4) Lazy loading support. (5) CDN with edge caching. (6) Progressive JPEG.

## Q14: What is `q_auto` in Cloudinary?
**A:** `q_auto` automatically selects the optimal compression quality for an image. Cloudinary analyzes the image content and selects a quality level that balances visual quality and file size. It can be tuned with presets: `q_auto:best`, `q_auto:good`, `q_auto:eco`, `q_auto:low`.

## Q15: What is `f_auto` in Cloudinary?
**A:** `f_auto` automatically serves the best image format based on the requesting browser's capabilities. It serves WebP for Chrome, AVIF for supported browsers, JPEG for others. This reduces bandwidth without code changes. Always recommended for production.

## Q16: What is `fl_progressive` in Cloudinary?
**A:** `fl_progressive` enables progressive JPEG rendering — the image loads in increasingly detailed passes. Variants: `fl_progressive:steep` (load first scan quickly), `fl_progressive:semi` (good balance), `fl_progressive:none` (baseline JPEG). Progressive images improve perceived performance.

## Q17: What are Cloudinary responsive breakpoints?
**A:** Cloudinary can automatically generate a set of image sizes (breakpoints) for responsive design. Using `w_auto` with a `dpr_auto` and responsive image tags, it serves appropriately sized images based on the device's viewport and pixel density. Use `srcset` attributes for implementation.

## Q18: What is Cloudinary's `srcset` generation?
**A:** Cloudinary can auto-generate HTML `<img>` `srcset` attributes with appropriate image sizes. The `c_scale,w_auto` transformation in combination with Cloudinary's responsive image helpers generates breakpoint URLs. This enables browsers to select the best-sized image.

## Q19: What is `dpr_auto` in Cloudinary?
**A:** `dpr_auto` automatically adjusts the image resolution based on the device's pixel ratio (1x, 2x, 3x). It detects the client's `devicePixelRatio` and serves accordingly. This ensures Retina/HiDPI displays get crisp images without wasting bandwidth on standard displays.

## Q20: What is Cloudinary Upload API?
**A:** The Upload API allows programmatic uploads of images and videos to Cloudinary. It supports direct upload (from server), remote fetch (from URL), base64 data, and unsigned uploads. Parameters include public ID, transformations, tags, folder, context, and eager transformations.

## Q21: What is the difference between signed and unsigned uploads?
**A:** **Signed uploads** require an API secret signature, providing security. Only authenticated clients (typically your server) can upload. **Unsigned uploads** use an upload preset and are useful for client-side uploads (from browsers/mobile apps) without exposing API secrets.

## Q22: What is an upload preset in Cloudinary?
**A:** An upload preset is a pre-defined set of upload parameters configured in the Cloudinary console. It enables unsigned uploads from clients by specifying defaults for folders, transformations, tags, moderation, and access control. Unsigned uploads reference a preset ID.

## Q23: What is Cloudinary's eager transformation?
**A:** Eager transformations are applied immediately after upload (in the background) rather than on first request. This pre-generates transformed versions so they are ready when first accessed, avoiding delay on the first request. Configured via `eager` parameter during upload.

## Q24: What is Cloudinary's incoming transformation?
**A:** Incoming transformations are applied to the original asset as it is uploaded. Unlike eager transformations (which create separate derived images), incoming transformations modify the original. The result replaces the original uploaded file.

## Q25: What is Cloudinary's fetch (remote) upload?
**A:** Cloudinary can fetch an image or video from an external URL using the Upload API with the `fetch` parameter. Cloudinary downloads the asset, stores it, and makes it available via the Cloudinary CDN. Example: `cloudinary.uploader.upload("https://example.com/image.jpg")`.

## Q26: What is Cloudinary's Admin API?
**A:** The Admin API provides administrative operations on your Cloudinary account: listing/managing assets, updating tags/context, creating folders, managing transformations, uploading presets, and accessing usage reports. It requires authentication with API key and secret.

## Q27: What is Cloudinary's Search API?
**A:** The Search API provides powerful asset discovery using expressions. It supports searching by public ID, folder, tags, context, filename, format, resource type, file size, dimensions, date ranges, and custom metadata. It returns paginated results with sort and aggregation options.

## Q28: What are Cloudinary tags?
**A:** Tags are labels attached to assets for organization and retrieval. An asset can have multiple tags. Tags are used in search, for creating image galleries, and for applying transformations to groups of assets (e.g., `if_tag` condition in transformations).

## Q29: What is Cloudinary context?
**A:** Context is key-value metadata attached to assets (e.g., `alt=Red Shoes`, `caption=Summer Collection 2024`). Unlike tags (many-to-many), context is structured data per asset. Context can be set during upload or via Admin API and used in search and delivery.

## Q30: What are Cloudinary folders?
**A:** Folders organize assets hierarchically. Public IDs can include folder paths (e.g., `products/shoes/red-shoe`). Folders help with organization, access control, and URL structure. They are created automatically when you upload with a folder path.

## Q31: What is Cloudinary's auto-upload feature?
**A:** Auto-upload automatically uploads images from an external source (AWS S3, Google Cloud Storage, or web server directory) to Cloudinary by configuring the external folder path. When a new file appears in the configured source, Cloudinary automatically uploads it.

## Q32: What is Cloudinary's moderation feature?
**A:** Cloudinary provides content moderation: (1) **Manual** — assets are held for human review. (2) **Automated** — AI-based moderation for inappropriate content (Metascore). (3) **ReKognition** or **Google Vision** — third-party AI moderation. Moderated assets can be approved, rejected, or automatically deleted.

## Q33: What is Cloudinary's AI Background Removal?
**A:** Cloudinary offers AI-powered background removal using deep learning. Simply add `e_background_removal` to the transformation URL. It automatically detects the main subject and removes the background. It works for people, products, and animals.

## Q34: What is Cloudinary's object-aware cropping?
**A:** Cloudinary's AI can detect objects and crop images based on specific object types. Using `c_crop,g_auto:subject`, Cloudinary identifies the main subject and crops around it. You can also specify custom object detection with `e_detect:object`.

## Q35: What are Cloudinary overlays?
**A:** Overlays allow layering one image, text, or video on top of another. Image overlays use `l_<public_id>` (layer). Text overlays use `l_text:<font>:<font_size>:<text>`. Position with `g_<gravity>`, `x_<offset>`, `y_<offset>`. Watermarks, logos, and captions are common uses.

## Q36: What is Cloudinary's text overlay?
**A:** Text overlays render text on images. Format: `l_text:Arial_30:Hello%20World,co_rgb:FFFFFF,g_south_east,x_10,y_10`. Parameters include font family, size, color, gravity, position, opacity, and background. Text can be styled with bold, italic, underline, and stroke.

## Q37: What are Cloudinary conditional transformations?
**A:** Conditional transformations apply only when specific conditions are met. Format: `if_<condition>/<transformation>/if_end`. Conditions include image dimensions (`if_w_gt_1000`), aspect ratio, file size, number of faces, and tags. Useful for applying different transformations based on image properties.

## Q38: What is Cloudinary's named transformation?
**A:** Named transformations allow saving a transformation string with a name for reuse. Instead of repeating long URLs, use `t_<name>` in the URL. Create via Admin API or console. Example: creating `t_thumbnail` as `c_fill,w_200,h_200`, then using `t_thumbnail` in URLs.

## Q39: What is Cloudinary's `e_improve` and `e_auto_brightness`?
**A:** `e_improve` (image enhancement) adjusts contrast and color to improve image appearance. `e_auto_brightness` automatically adjusts brightness. `e_auto_contrast` adjusts contrast. These provide one-click image enhancement without manual parameter tuning.

## Q40: What is Cloudinary's `e_vignette` and `e_sepia`?
**A:** `e_vignette` applies a vignette effect (darkens edges). `e_sepia` applies a sepia tone filter. Cloudinary offers dozens of artistic effects including: `e_art:audrey` (Instagram-like filters), `e_cartoonify`, `e_oil_paint`, `e_blur`, `e_grayscale`, `e_negate`, `e_pixelate`, `e_sharpen`, `e_unsharp_mask`.

## Q41: What is Cloudinary's face detection?
**A:** Cloudinary can detect faces in images and apply transformations based on them. Features: `g_face` (crop to face), `e_blur_faces` (blur faces for privacy), `if_face_count` (conditional on number of faces), `l_<image>:g_face` (overlay on face position).

## Q42: What is Cloudinary's cropping methods for videos?
**A:** Video cropping in Cloudinary includes: `c_fill` (resize and crop), `c_fit` (fit within dimensions), `c_crop` (exact crop), `c_pad` (add padding), `c_thumb` (thumbnail with gravity). Video-specific: `c_scale`, `c_limit`, `e_trim` (trim black bars).

## Q43: How does Cloudinary handle video transcoding?
**A:** Cloudinary automatically transcodes uploaded videos using configurable parameters: codec (`vc_h264`, `vc_vp9`, `vc_hevc`), video bitrate (`b_1500k`), audio bitrate (`ab_128k`), frame rate (`fps_30`), resolution, aspect ratio, and keyframe interval.

## Q44: What is Cloudinary's video trimming?
**A:** Video trimming extracts a portion of the video using `so_<start_offset>` (start offset) and `eo_<end_offset>` (end offset). Example: `so_2.5_eo_15.5` trims from 2.5s to 15.5s. Durations can be in seconds or percentage (`so_10p`).

## Q45: What is Cloudinary's video concatenation?
**A:** Video concatenation joins multiple video clips using overlay/chaining. Videos can be concatenated with crossfade transitions (`e_transition`). Example: Upload multiple videos, then use `e_transition` in the transformation URL to create a seamless compilation.

## Q46: What is Cloudinary's video adaptive streaming?
**A:** Cloudinary supports adaptive streaming formats: HLS (HTTP Live Streaming) and MPEG-DASH. These break videos into segments at multiple bitrates, allowing players to switch quality based on network conditions. Use `fl_hls` or `fl_dash` in transformations.

## Q47: What is Cloudinary's sprite generation?
**A:** Sprites combine multiple images into a single composite image (sprite sheet). Use `e_sprite` with `c_fill,w_50,h_50` to specify layout. CSS offsets for each frame are returned. Useful for CSS sprites for icons, thumbnails, or animations.

## Q48: What is Cloudinary's `fl_animated`?
**A:** `fl_animated` converts a sequence of images or a video into an animated GIF. Combine with `pg_3` (frame delay) and `loop` (loop count). Example: `fl_animated,pg_3,w_300,c_fill` creates a looping GIF from multiple source images.

## Q49: What are Cloudinary `f_webp` and `f_avif`?
**A:** `f_webp` converts images to WebP format (Google, smaller than JPEG/PNG). `f_avif` converts to AVIF format (based on AV1 codec, even smaller). Both support transparency and animation. Use `f_auto` to let Cloudinary choose the best format automatically.

## Q50: What is Cloudinary's `pg_` parameter?
**A:** `pg_` (page) is used for multi-page assets (PDFs, PSDs, animated GIFs). `pg_1` selects the first page. `pg_all` flattens all pages. Used with `e_sprite` for sprite generation. PDFs can be converted page-by-page to images.

## Q51: What is Cloudinary's color overlay?
**A:** Color overlays apply a color tint over the entire image using `e_tint:<color>` or `e_colorize:<level>` with `co_<color>`. Example: `e_colorize:60,co_blue` applies a 60% blue colorize. This is used for product color variants and branding.

## Q52: What is Cloudinary's `e_cartoonify`?
**A:** `e_cartoonify` applies a cartoon effect with configurable line strength and color reduction. Parameters: `e_cartoonify:<line_strength>:<color_reduction>`. Example: `e_cartoonify:15:30`. Creates a cartoon-style rendering of the original image.

## Q53: What is Cloudinary's `e_pixelate`?
**A:** `e_pixelate` pixelates regions of an image. Can be applied globally or to specific regions (e.g., faces for privacy). `e_pixelate_faces` blurs/pixelates all detected faces automatically. Used for anonymizing people in images.

## Q54: What is Cloudinary's image upscaling?
**A:** Cloudinary can upscale images using AI-powered `e_upscale` transformation. It increases image resolution while preserving detail using deep learning super-resolution. Useful for improving low-resolution images.

## Q55: What are Cloudinary SDKs?
**A:** Cloudinary provides SDKs for popular languages and frameworks: JavaScript (React, Vue, Angular, Node.js), Python, Ruby, PHP, Java, .NET, Go, iOS, and Android. SDKs simplify URL generation, upload, and API interactions with native language bindings.

## Q56: What is Cloudinary's JavaScript SDK (`cloudinary-core`)?
**A:** The JavaScript SDK provides client-side functionality: generating transformation URLs, uploading images directly from the browser (unsigned with upload preset), and client-side image manipulation. The newer `@cloudinary/url-gen` SDK provides a programmatic URL generation API.

## Q57: What is Cloudinary's React SDK?
**A:** Cloudinary offers `@cloudinary/react` and `@cloudinary/url-gen` for React apps. Components include `<CloudinaryImage>`, `<CloudinaryVideo>`, and `<AdvancedImage>`. It supports responsive images, lazy loading, placeholders, and transformation chaining with a declarative API.

## Q58: What is Cloudinary's Angular SDK?
**A:** `@cloudinary/angular` provides Angular components and services for integrating Cloudinary. Includes `<cl-image>` and `<cl-video>` components with transformation directives. Supports Angular's change detection, lazy loading, and responsive images.

## Q59: What is Cloudinary's Vue SDK?
**A:** `cloudinary-vue` provides Vue components (`<cld-image>`, `<cld-video>`, `<cld-placeholder>`) for integration with Vue 2 and 3. It supports transformations, responsive images, and Cloudinary's image optimization features through Vue's template syntax.

## Q60: What is Cloudinary's Node.js SDK?
**A:** The Node.js SDK (`cloudinary`) provides server-side functionality: upload (local files, remote URLs, base64), admin operations, search, URL generation, and transformation chaining. It uses the `cloudinary.config()` to set cloud name, API key, and API secret.

## Q61: What is Cloudinary's Python SDK?
**A:** The Python SDK (`cloudinary`) is for server-side integration. Features: `cloudinary.uploader.upload()`, `cloudinary.api.resources()`, `cloudinary.CloudinaryImage()` for URL generation, and `cloudinary.Search()` for asset discovery. Configured via `cloudinary.config()`.

## Q62: What is Cloudinary's `.image()` and `.video()` URL builders?
**A:** SDKs provide URL builder methods: `.image('public_id')` generates an image URL. `.video('public_id')` generates a video URL. Both accept transformation parameters. Example (Python): `cloudinary.CloudinaryImage("sample.jpg").image(width=300, height=200, crop="fill")`.

## Q63: What is Cloudinary's SEO-friendly URLs?
**A:** Cloudinary supports SEO-friendly URLs by using meaningful filenames instead of random public IDs. During upload, set a descriptive public ID. URLs can include keywords: `https://res.cloudinary.com/demo/image/upload/red-shoes-summer-2024.jpg`. Transformations can be appended without breaking SEO.

## Q64: What is Cloudinary's `fl_attachment`?
**A:** `fl_attachment` forces the browser to download an asset instead of displaying it. The download filename can be set with the `fl_attachment:filename.ext` syntax. Used for providing downloadable assets (PDFs, high-resolution images).

## Q65: What is Cloudinary's CORS configuration?
**A:** CORS (Cross-Origin Resource Sharing) must be configured in the Cloudinary console for client-side uploads from browser applications. You specify allowed origins, methods, and headers. Without proper CORS, browser-based uploads will fail.

## Q66: What is Cloudinary's CDN?
**A:** Cloudinary uses a global CDN (Content Delivery Network) powered by Akamai for fast media delivery worldwide. Assets are cached at edge locations close to users. Cache headers and versioning help control caching behavior.

## Q67: What is Cloudinary's cache invalidation?
**A:** Cloudinary caches transformed images at CDN edge locations. To invalidate the cache: (1) Change the version parameter in the URL (`v123`), (2) Use `invalidate: true` when updating an asset, (3) Use the Admin API's `uploader.remove_cached_urls` or `api.delete_derived_resources`.

## Q68: What is Cloudinary's version parameter (`v`)?
**A:** The version parameter in Cloudinary URLs is a Unix timestamp (e.g., `v1712345678`) representing when the asset was last updated. It acts as a cache buster — incrementing the version forces CDN re-fetch. Use it to ensure fresh content is delivered after updates.

## Q69: What is Cloudinary's resource type?
**A:** Resource type categorizes assets: `image` (JPEG, PNG, GIF, WebP, SVG, etc.), `video` (MP4, MOV, AVI, WebM, etc.), `raw` (PDF, DOC, ZIP, font files, etc.), `auto` (automatically detect type). It is the first path segment after cloud name in URLs.

## Q70: What is Cloudinary's type parameter?
**A:** The type parameter indicates how the asset was added: `upload` (uploaded via API/console), `fetch` (fetched from URL), `private` (access-restricted), `authenticated` (requires signed URLs), `facebook`, `twitter`, `youtube` (imported from social media), `gravatar` (imported from Gravatar).

## Q71: What are private and authenticated assets in Cloudinary?
**A:** **Private** assets require a signed URL for access — they are not accessible via the standard URL. **Authenticated** assets require signed URLs and have stricter access control. Both are used for access-restricted content. Signed URLs include a signature parameter in the URL.

## Q72: What is Cloudinary's signed URL?
**A:** A signed URL includes a digital signature created using your API secret. Only users with the signed URL can access private or authenticated assets. The signature can include expiration time for temporary access. Generate via SDK or manually.

## Q73: What is Cloudinary's default image?
**A:** Cloudinary can serve a default image when an asset is not found. Use the `d_<public_id>` parameter in the URL. Example: `d_default-image.jpg` — if the requested asset doesn't exist, Cloudinary serves the specified default instead of a 404 error.

## Q74: What is Cloudinary's overlay with text from URL?
**A:** Overlays can use text directly from a URL parameter or from a remote text file. Example: `l_text:Arial_30:<url_encoded_text>,co_white,g_south_east`. For dynamic text, use SDKs to programmatically insert text into overlay URLs.

## Q75: What is Cloudinary's watermark?
**A:** Watermarks are implemented using overlays. Upload a logo as an asset, then overlay it on images using `l_logo,g_south_east,x_10,y_10,o_60` (position and opacity). Watermarks can be applied automatically via upload presets or transformations.

## Q76: What is Cloudinary's `e_trim`?
**A:** `e_trim` automatically removes empty bordering whitespace (or near-whitespace) from images. Configurable with `e_trim:<tolerance>` where higher tolerance removes more. Useful for product photos with white backgrounds.

## Q77: What is Cloudinary's `e_shadow`?
**A:** `e_shadow` adds a realistic drop shadow to the subject of an image. Parameters: `e_shadow:<x_offset>,<y_offset>,<blur>,<opacity>`. Creates a shadow behind the main subject. Works best on images with transparent backgrounds.

## Q78: What is Cloudinary's `e_outline`?
**A:** `e_outline` extracts the outline/shape of the main subject. Parameters: `e_outline:<mode>,<width>,<color>`. Modes include `inner` and `outer`. Useful for creating stickers or cutout effects from images with transparent backgrounds.

## Q79: What is Cloudinary's `e_art` filters?
**A:** Cloudinary offers art filters (like Instagram filters) via `e_art:<filter>`. Options include: `al_dente`, `athena`, `audrey`, `aurora`, `daguerre`, `eucalyptus`, `fes`, `frost`, `hairspray`, `hokusai`, `incognito`, `lsr`, `peacock`, `primavera`, `quartz`, `red_rock`, `refresh`, `sizzle`, `sonnet`, `ukulele`, `zorro`.

## Q80: What is Cloudinary's metadata management?
**A:** Cloudinary's structured metadata allows defining custom metadata fields (text, integer, date, enum, set) attached to assets. Fields are defined in the console and populated during/after upload via API. Metadata can be searched, filtered, and displayed.

## Q81: What is Cloudinary's webhook notifications?
**A:** Cloudinary can send HTTP notifications (webhooks) when specific events occur: upload completion, deletion, moderation result, or eager transformation completion. Configure notification URLs in the console. The webhook payload contains asset details.

## Q82: What is Cloudinary's backup feature?
**A:** Cloudinary can automatically back up all uploaded original assets to an external storage (AWS S3, Google Cloud Storage, or FTP server). Backups include metadata. Configure the backup URL in the Cloudinary console. This provides off-site disaster recovery.

## Q83: What is Cloudinary's usage and billing?
**A:** Cloudinary pricing is based on: (1) Total storage (GB of original + derived assets). (2) Bandwidth (GB transferred). (3) Transformations (number of derived images generated). (4) Video processing (seconds of video). (5) AI credits (for AI features). Free tier includes 25GB storage and 25GB bandwidth.

## Q84: What are Cloudinary's security best practices?
**A:** (1) Keep API secret confidential — never expose in client-side code. (2) Use signed uploads from servers. (3) For client uploads, use unsigned uploads with upload presets (limit allowed folders). (4) Restrict transformations to prevent abuse. (5) Use private/authenticated assets for sensitive content. (6) Enable HTTPS-only delivery.

## Q85: What is Cloudinary's signed URLs with expiration?
**A:** Signed URLs can include an expiration timestamp. After the expiration, the URL becomes invalid. Example (Node.js): `cloudinary.url("image.jpg", {sign_url: true, type: "authenticated", resource_type: "image", expires_at: Math.floor(Date.now()/1000) + 3600})`.

## Q86: How do you handle image uploads from mobile apps in Cloudinary?
**A:** Mobile apps use unsigned uploads with an upload preset. The SDK (iOS/Android) uploads directly from the device to Cloudinary. The upload preset specifies folders, eager transformations, and moderation. The server receives the uploaded asset's public ID and can then associate it with the user.

## Q87: What is Cloudinary's auto-tagging?
**A:** Cloudinary can automatically tag uploaded images using AI-based image recognition (Google Vision, ReKognition, or Cloudinary's own AI). Auto-tags describe image content (e.g., "beach", "sunset", "car"). Tags enable automatic categorization and search.

## Q88: What is Cloudinary's OCR (Optical Character Recognition)?
**A:** Cloudinary can extract text from images using OCR via Google Vision integration. Text can be searched and used for auto-tagging. The `e_ocr` transformation or upload parameter enables text extraction. Extracted text is stored in image metadata.

## Q89: What is Cloudinary's `e_watermark` vs overlay?
**A:** `e_watermark` is a dedicated watermark transformation that applies a pre-configured watermark image stored in your account. Overlay (`l_`) is a general mechanism. The watermark approach is simpler for consistent branding; overlays offer more flexibility (position, opacity, size).

## Q90: How does Cloudinary handle EXIF data?
**A:** Cloudinary preserves EXIF data during upload. By default, images are auto-oriented based on EXIF orientation tag. EXIF data can be retrieved via the Admin API. Use `fl_strip_profile` to remove EXIF/profiles to reduce file size (at the cost of losing metadata).

## Q91: What is Cloudinary's `co_` (color) parameter?
**A:** The `co_` parameter specifies colors in transformations. Formats: RGB hex (`co_rgb:ff0000`), named colors (`co_red`, `co_white`, `co_black`), with opacity (`co_rgb:ff0000_50`). Used with: text overlays, tinting, borders, backgrounds, and effects.

## Q92: What is Cloudinary's `bo_` (border) parameter?
**A:** `bo_` adds a border around images. Format: `bo_<width>px_solid_<color>`. Example: `bo_5px_solid_rgb:333333`. Borders can be applied as part of transformations for framing images, profile pictures, or thumbnails.

## Q93: What is Cloudinary's `e_loop` for videos?
**A:** `e_loop` controls video looping. `e_loop` (loop infinitely), `e_loop:3` (loop 3 times). Combined with `fl_animated` for GIF creation. Useful for short video clips and background videos.

## Q94: What is Cloudinary's `e_preview` for videos?
**A:** `e_preview` generates a preview video from a portion of the video timeline. Parameters: `e_preview:<duration>:<segment_count>` or just `e_preview` for automatic. Creates a short, engaging preview clip. Useful for video thumbnails and previews in galleries.

## Q95: How do you migrate from another CDN/image service to Cloudinary?
**A:** (1) Use the Upload API with `fetch` to pull existing assets from URLs. (2) Use `cloudinary-migration` scripts or custom scripts to batch upload with original timestamps. (3) Update application URLs to Cloudinary URLs. (4) Configure existing CDN URLs to redirect to Cloudinary. (5) Test and cut over DNS.

## Q96: What is Cloudinary's URL-based API?
**A:** Cloudinary's URL-based API allows performing operations by simply modifying the URL — no code changes needed for transformations. Every transformation parameter (resize, crop, format, effect, overlay) corresponds to URL parameters. This is Cloudinary's core architectural principle.

## Q97: What are Cloudinary's analytics?
**A:** Cloudinary provides analytics on: (1) Bandwidth usage over time. (2) Storage consumption. (3) Most accessed assets. (4) Transformation counts. (5) Geographic distribution of requests. Analytics are available in the console dashboard and via Admin API.

## Q98: What is Cloudinary's Media Library?
**A:** The Media Library is Cloudinary's web-based Digital Asset Management (DAM) interface. It provides: asset browsing (grid/list), search, tagging, folder management, preview, basic editing, upload, download, and embedding copy functionality. It is accessible in the Cloudinary console.

## Q99: How does Cloudinary integrate with frameworks (Next.js, Gatsby, etc.)?
**A:** Cloudinary provides plugins for: **Next.js** — `@cloudinary/next` for optimized images with Next.js Image component. **Gatsby** — `gatsby-plugin-cloudinary` and `gatsby-transformer-cloudinary`. **Nuxt.js** — `@nuxtjs/cloudinary`. **Hugo** — shortcodes. **Eleventy** — plugins. These provide automatic optimization and lazy loading.

## Q100: What is Cloudinary's architecture diagram pattern?
**A:** The typical Cloudinary integration flow: (1) Client sends media to Cloudinary (direct upload from browser, or server upload). (2) Cloudinary stores and processes the asset (AI analysis, auto-tagging, eager transformations). (3) Server stores the returned public ID in the database. (4) Application generates Cloudinary URLs with transformations for delivery. (5) Cloudinary serves transformed assets via global CDN. (6) If asset is updated, server invalidates cache and Cloudinary CDN re-caches.
