# Text-to-Speech API Documentation

This API provides a text-to-speech service that generates audio files from text input. It supports multiple languages and processes requests sequentially using a queue mechanism.

## API Endpoints

### 1. Generate Audio

**Endpoint:** `/generate_audio`  
**Method:** `POST`  
**Description:** Generates an audio file from the provided text input.

**Request JSON Format:**

```json
{
    "text": "Your text here",
    "lang": "en" // or "vi" for Vietnamese
}
```

**Response JSON Format:**

```json
{
    "message": "Audio generated successfully",
    "file_url": "http://127.0.0.1:5000/download/your_generated_file.wav",
    "duration": 2.345 // Time taken to generate the audio in seconds
}
```

### 2. Download Audio

**Endpoint:** `/download/<filename>`  
**Method:** `GET`  
**Description:** Downloads the generated audio file.

**Example URL:**

```
http://127.0.0.1:5000/download/your_generated_file.wav
```

## Usage Example

### Generate Audio

To generate audio, send a POST request to the `/generate_audio` endpoint with the following JSON payload:

```json
{
    "text": "Hello, world!",
    "lang": "en"
}
```

#### Curl Example

```bash
curl -X POST http://127.0.0.1:5000/generate_audio -H "Content-Type: application/json" -d '{"text":"Hello, world!","lang":"en"}'
```

The response will include a URL to download the generated audio file.

### Download Audio

To download the generated audio, use the URL provided in the response from the `/generate_audio` endpoint.

For example:

``http://127.0.0.1:5000/download/your_generated_file.wav``

## Notes

- The `lang` parameter supports `"en"` for English and `"vi"` for Vietnamese.
- The server processes requests sequentially, so users may experience longer wait times if multiple requests are made simultaneously.
- Ensure the `output` directory is writable and has sufficient space for storing generated audio files.

For further questions or issues, please contact the repository owner or maintainer.