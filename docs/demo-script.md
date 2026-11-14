# DeepGuard demo script (about 4 minutes)

## Before the demo
1. Start Docker Desktop and wait until it says "Engine running".
2. In the project folder run `docker compose up` at least 10 minutes before the demo.
3. Open http://localhost:8000 and http://localhost:8000/docs in the browser.
4. Keep these files in one folder: real_clip.mp4, fake_clip.mp4, real_voice.wav, fake_voice.wav, real_text.txt, fake_text.txt.
5. Keep the screen recording and the screenshots ready as a backup.

## Steps
| Time | Do | Say |
|---|---|---|
| 0:00 | Show the architecture (Methodology slide) | Five parts: web page, gateway, job queue, model services, ensemble. |
| 0:30 | Open http://localhost:8000 | This page is served by our gateway. |
| 0:45 | Upload real_clip.mp4, real_voice.wav, real_text.txt and press Analyze | The gateway detects each file type, creates a job and routes every file to its model container. |
| 1:30 | Show the result: REAL | Each model gives a score. Voting and weighted averaging combine them into one verdict. |
| 2:00 | Upload fake_clip.mp4, fake_voice.wav, fake_text.txt | Same flow, this time the verdict is FAKE. |
| 2:30 | Point at Recent jobs | Every job and result is stored in PostgreSQL. |
| 2:45 | Terminal: `docker compose ps` | Seven containers: gateway, database, Redis and four model services. |
| 3:00 | `docker compose stop video-model-b`, upload fake_clip.mp4, then `docker compose start video-model-b` | If one model is down, the job still finishes with the other models. |
| 3:30 | Open http://localhost:8000/docs | The API documentation is generated automatically. |
| 3:50 | Say it clearly | Model scores are simulated. Group 1's trained models plug into the same interface. |

## Expected results
| Files | Verdict |
|---|---|
| Only real_ files | REAL, confidence about 70 to 98 percent |
| Only fake_ files | FAKE, confidence about 70 to 98 percent |
| fake_clip.mp4 + real_voice.wav | FAKE, confidence about 60 percent |

## If something fails
Play the screen recording. Do not debug in front of the panel.
