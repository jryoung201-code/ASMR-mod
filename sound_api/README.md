# Quiet Craft sound API

This HTTP service stores audio on the server filesystem and reads catalog metadata through the Google Sheets API. It runs independently of Minecraft. The current mod still plays Minecraft's built-in sounds.

## Prepare the catalog

1. Create a Google spreadsheet, name its tab `Sounds`, and paste the header from [catalog-template.csv](catalog-template.csv) into A1:E1.
2. In Google Cloud, enable the [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) and give the API host a Google service account. Share the spreadsheet with the service account email as **Viewer**. Keep the spreadsheet private if desired.
3. Set `ASMR_SPREADSHEET_ID` to the ID between `/d/` and the next slash in the Sheet URL. Configure [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) on the host. For local use with a service-account key, set `GOOGLE_APPLICATION_CREDENTIALS` to its absolute path outside the repo.
4. Put audio files in `sound_api/audio/` or set `ASMR_AUDIO_DIR` to the absolute path of a persistent audio directory. Update the sheet to publish them. The API checks Google Sheets at most once every 30 seconds per process.

| Column | Format |
| --- | --- |
| id | Unique lowercase identifier such as `soft-rain` |
| title | Display name |
| filename | Exact filename, with no directories. Supports OGG, WAV and MP3 |
| category | Group name such as `rain` |
| enabled | `TRUE` publishes the file, `FALSE` or blank hides it |

Enabled rows with missing files are omitted from the catalog. Public API clients can read and download enabled sounds. Edit metadata in Sheets and upload files through your hosting provider's normal file-management tools.

## Run the API

Use Python 3.10 or later. From the repo root, with the environment configured as above, run:

```sh
python -m pip install -r sound_api/requirements.txt
python -m waitress --listen=127.0.0.1:8080 --call sound_api.app:create_app
```

- `GET /health` checks that the HTTP process is responding.
- `GET /api/v1/sounds` returns the published catalog and relative audio URLs.
- `GET /api/v1/sounds/<id>/audio` serves the audio file. Supports HTTP byte ranges for seeking.

For a shared deployment, put the API behind an HTTPS proxy and place audio on a persistent volume. Keep credentials private and commit neither audio files nor service-account keys.
