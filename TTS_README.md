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
    "lang": "en",
    "voice_name": "default",
    "user_id": "1",
    "user_type": "user",
    "preset": "ultra_fast"
}
```

**Response JSON Format:**

```json
{
    "message": "Audio generated successfully",
    "file_url": "http://127.0.0.1:5000/download/user/user123/1629123456_default_a1b2c3d4.wav",
    "audio_name": "1629123456_default_a1b2c3d4.wav",
    "audio_size": 12345,
    "audio_path": "/path/to/output/user/user123/1629123456_default_a1b2c3d4.wav",
    "generation_time": 2.345,
    "audio_duration": 3.5,
    "audio_wavelength": 3.5,
    "user_type": "user",
    "user_id": "user123",
    "voice_name": "default",
    "language": "en",
    "preset": "ultra_fast",
    "timestamp": 1629123456,
    "text_length": 12,
    "mime_type": "audio/wav",
    "sample_rate": 24000
}
```

### 2. Download Audio

**Endpoint:** `/download/<user_type>/<user_id>/<filename>`  
**Method:** `GET`  
**Description:** Downloads the generated audio file.

**Example URL:**

```bash
http://127.0.0.1:5000/download/user/user123/1629123456_default_a1b2c3d4.wav
```

## Usage Example

### Generate Audio

To generate audio, send a POST request to the `/generate_audio` endpoint with the following JSON payload:

```json
{
    "text": "Hello, world!",
    "lang": "en",
    "voice_name": "default",
    "user_id": "user123",
    "user_type": "user",
    "preset": "ultra_fast"
}
```

#### Curl Example

```bash
curl -X POST http://127.0.0.1:5000/generate_audio \
     -H "Content-Type: application/json" \
     -d '{
         "text": "Hello, world!",
         "lang": "en",
         "voice_name": "default",
         "user_id": "user123",
         "user_type": "user",
         "preset": "ultra_fast"
     }'
```

The response will include a URL to download the generated audio file.

### Download Audio

To download the generated audio, use the URL provided in the response from the `/generate_audio` endpoint.

```bash
curl -O http://127.0.0.1:5000/download/user/user123/1629123456_default_a1b2c3d4.wav

```

## Notes

- The `lang` parameter supports `"en"` for English and `"vi"` for Vietnamese.
- The server processes requests sequentially, so users may experience longer wait times if multiple requests are made simultaneously.
- Ensure the `output` directory is writable and has sufficient space for storing generated audio files.

For further questions or issues, please contact the repository owner or maintainer.
