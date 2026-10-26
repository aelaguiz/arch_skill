# Setup: the channel's grant

## What exists

- **The channel:** Poker Skill, `@pokerskill_`, channel id `UCTnx-FepuY_x-QGQIxWNSVA`. It is the YouTube channel of the Google account amir@fun.country itself, not a separate brand account, so signing in as that account reaches it with no channel picker.
- **The grant:** a signed-in OAuth grant made October 26, 2026, stored in the secrets repo at `~/workspace/secrets/local/services/youtube/pokerskill-channel-oauth.json` (Google's `authorized_user` JSON: client id, client secret, refresh token). `YOUTUBE_OAUTH_FILE` points the helper elsewhere. Never print it, copy it into a project, or paste it anywhere.
- **The OAuth client:** the work client "Poker Skill Stats" in Google Cloud project `poker-skill-a2d33`, internal to the fun.country organization, the same client the `gws` CLI uses (`~/workspace/secrets/local/google/gws-client_secret-poker-skill-a2d33.json`; `YOUTUBE_CLIENT_FILE` overrides). Because the client is internal, the refresh token has no seven-day testing expiry and no "unverified app" screen.
- **The APIs:** YouTube Data API v3, YouTube Analytics API and YouTube Reporting API are switched on in `poker-skill-a2d33`, so every call's quota is that project's (10,000 units a day plus the upload and search buckets).
- **Scopes:** `youtube`, `youtube.upload`, `youtube.force-ssl` (captions and comments) and `yt-analytics.readonly`. Revenue metrics would need `yt-analytics-monetary.readonly` and a channel in the YouTube Partner Program; the channel isn't in it.

## Check it

```bash
python3 "{baseDir}/scripts/yt.py" whoami
```

It prints the channel, its counts and the grant's scopes. `invalid_grant` means the grant was revoked or expired; sign in again.

## On another machine

The secrets repo is enrolled on the fleet's machines. Restore the grant there from its encrypted copy, from the repo root:

```bash
./bin/secrets decrypt services/youtube/pokerskill-channel-oauth.json
```

Then `whoami`. Don't copy the plaintext between machines by any other route.

## Sign in again

Only when the grant is gone or revoked. The browser that opens the address must be signed in to Google as amir@fun.country (in BrowserOS, the `Work` profile; follow `$browseros` for opening the page in that profile's window without taking focus):

```bash
python3 "{baseDir}/scripts/yt.py" login --url-file <private file outside any repo>
```

It writes the Google sign-in address to the file (mode 600) and waits up to 15 minutes on a localhost port. Open the address in a background tab of the `Work` window, choose amir@fun.country, then Allow. Google's account chooser in a background tab may ignore clicks until focus emulation is on for that page and the page is reloaded. The helper saves the new grant over the old one and prints the channel it reached. Then encrypt and commit the new copy in the secrets repo (`./bin/secrets encrypt services/youtube/pokerskill-channel-oauth.json`, `./bin/secrets check`, commit only the encrypted file), and delete the file holding the sign-in address.

## Revoke

Google Account of amir@fun.country › Security › Third-party access › Poker Skill Stats › remove access, only with Amir's approval. It removes this grant and the `gws` CLI's grants on the same client.
