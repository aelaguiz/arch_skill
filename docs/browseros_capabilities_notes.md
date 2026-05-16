# BrowserOS Capability Notes

Living notes for what we learn while mapping BrowserOS MCP behavior and its
on-disk state. Append new findings under dated entries.

## 2026-05-02 - Profile Directory To Display Name

BrowserOS MCP reports the Chromium profile directory name in
`browserContextId`.

Observed open windows:

- `browserContextId: "Default"` maps to BrowserOS profile name `Work`.
- `browserContextId: "Profile 1"` maps to BrowserOS profile name `pro6`.

The mapping lives in Chromium's global profile registry:

```text
/Users/aelaguiz/Library/Application Support/BrowserOS/Local State
```

Use this command to list profile directory names and display names:

```bash
rtk jq -r '.profile.info_cache | to_entries[] | "\(.key)\t\(.value.name)"' \
  "/Users/aelaguiz/Library/Application Support/BrowserOS/Local State"
```

Current confirmed output:

```text
Default    Work
Profile 1 pro6
```

Important distinction:

- `Profile 1` is the on-disk/internal Chromium profile id.
- `pro6` is the user-facing BrowserOS/Chromium profile display name.
- The display-name mapping is in `Local State`, not in
  `Profile 1/Preferences`.

Related BrowserOS app state exists under:

```text
/Users/aelaguiz/Library/Application Support/BrowserOS/.browseros/
```

That directory includes `browseros.db`, with tables including `identity`,
`oauth_tokens`, and `rate_limiter`. The BrowserOS profile display-name mapping
above was not found there. Do not dump token values while inspecting it.

## 2026-05-02 - BrowserOS CDP Port And Google Sign-In

BrowserOS exposes its local Chromium DevTools Protocol port in:

```text
/Users/aelaguiz/Library/Application Support/BrowserOS/.browseros/server_config.json
```

Observed values:

```json
{
  "ports": {
    "cdp": 9101,
    "extension": 9300,
    "server": 9200
  }
}
```

The local CDP endpoint is:

```text
http://127.0.0.1:9101/json/list
```

Useful behavior:

- BrowserOS MCP `list_pages` returns a `targetId`.
- The same `targetId` appears as `id` in the CDP `/json/list` output.
- CDP can therefore attach to the exact same tab that BrowserOS MCP sees.

Observed limitation:

- BrowserOS MCP `fill`, `type_at`, and `press_key` did not reliably mutate the
  Google sign-in email field during this run.
- `evaluate_script` could set DOM state, but that alone is not enough for every
  Google sign-in transition.
- Direct CDP input through `Input.insertText` plus
  `Input.dispatchMouseEvent` successfully submitted the identifier form.

Google sign-in result observed for `pro6@fun.country`:

```text
Couldn’t find your Google Account
```

Because Google stopped at the identifier step, the password-change flow was not
reachable in this run.

## 2026-05-02 - Forced Google Password Change

After the correct current password was entered manually, Google moved the
`Profile 1` tab to the forced password-change form:

```text
https://accounts.google.com/v3/signin/speedbump/changepassword/changepasswordform
```

BrowserOS MCP snapshot exposed the relevant controls cleanly:

- `Create password`
- `Confirm`
- `Show password`
- `Next`

Direct CDP input worked for this form:

- Focus the first visible `input[type=password]`.
- Insert the new password with `Input.insertText`.
- Focus the second visible `input[type=password]`.
- Insert the same password with `Input.insertText`.
- Click the `Next` button with `Input.dispatchMouseEvent`.

Successful result:

```text
https://mail.google.com/mail/u/0/#inbox
```

Secret-handling note:

- A dotenv/env file may quote password values.
- Shell-sourcing the file can change the effective value when special
  characters are present.
- For browser automation, parse the secret file as data and pass the exact
  value to CDP. Do not print the secret while checking length, quoting, or
  field-fill behavior.

## 2026-05-02 - ChatGPT Signup With Google SSO

BrowserOS MCP handled this flow with ordinary page snapshots, clicks, and fills:

- Google search for `chatgpt`.
- Click the organic `chatgpt.com` result.
- Submit a public test prompt on the logged-out ChatGPT page.
- Open `Sign up for free`.
- Choose `Continue with Google`.
- Select the already logged-in Google Workspace account in `Profile 1`.
- Finish the ChatGPT account profile/onboarding.

Observed result:

```text
https://chatgpt.com/
```

The signed-in page showed profile `Pro Six` and a usable ChatGPT prompt box.

## 2026-05-02 - Ramp Product Virtual Card Flow

BrowserOS MCP was enough for the Ramp card-issue flow in the `Default` profile:

- `list_windows` showed `Default` as the work/Ramp browser context.
- `list_pages` found the live Ramp tab at `https://app.ramp.com/...`.
- `take_snapshot`, `click`, and `fill` were enough to create and edit the card.

Observed Ramp path:

- Open `Manage spend` -> `Cards`.
- Click `Issue`.
- Choose `Product or service`.
- Set vendor/product to `OpenAI`.
- Set amount to `$250`.
- Set frequency to `Monthly`.
- Issue the virtual card.

Observed naming convention:

- Existing rows used `Pro - Pro1` through `Pro - Pro5`.
- The new card was therefore renamed to `Pro - Pro6`.

Ramp edit note:

- Newly issued product/service cards may first appear under the vendor/product
  name, such as `OpenAI`.
- Open the row drawer, then use `Actions` -> `Edit`.
- The display name is controlled by the `What is it for?` field.
- After changing that field, the save may complete and leave `Save changes`
  disabled; using `Back` from the edit drawer refreshed the list row with the
  new name.

## 2026-05-02 - Stripe Payment Fields Inside ChatGPT Checkout

ChatGPT checkout used a Stripe payment iframe for card entry. BrowserOS MCP
could see the outer page and the iframe, but ordinary paste did not populate
the secure card fields during this run.

Working input path:

- Use Ramp's secure copy controls for card number, expiry, and CVC.
- Focus the relevant Stripe field in the ChatGPT checkout by page coordinates.
- Read the copied value as data, validate only its shape and length, and do not
  print it.
- Send one character at a time to the ChatGPT page target through CDP
  `Input.insertText`.

Observed result:

- Card number accepted as 16 typed characters.
- Expiry accepted as 4 typed characters.
- CVC accepted as 3 typed characters.

Safety note:

- Do not log or save payment values.
- Keep the final purchase action separate from card-field entry so the user can
  explicitly confirm the charge before clicking `Subscribe`.

## 2026-05-02 - ChatGPT Checkout Billing Address

After the Stripe card fields were filled, ChatGPT revealed a billing address
section lower on the checkout page.

Working address path:

- Use Ramp's card drawer copy controls for the billing name and address pieces.
- Type copied values into the ChatGPT/Stripe checkout fields through focused
  browser input, not broad DOM mutation.
- The `Address` field opened Google-powered address suggestions.
- Selecting the Austin suggestion split the address into line 1, line 2, city,
  state, and ZIP fields.

Observed checkout behavior:

- Before the billing address was filled, ChatGPT showed no estimated tax and
  `$8.00` due today for the Go plan.
- After the Austin, Texas billing address was selected, ChatGPT showed `Sales
  Tax (6.4%)` and `$8.51` due today.
- The final `Subscribe` button remained a separate purchase action.

Final purchase confirmation:

- The user explicitly authorized clicking `Subscribe` for this specific
  ChatGPT Go checkout and asked not to be prompted again for that checkout.
- After `Subscribe` was clicked, ChatGPT returned to the main app.
- The profile menu showed `Pro Six Go`, confirming the account was on the Go
  plan.

## 2026-05-02 - ChatGPT Go First, Then Pro Upgrade Rule

The process for new ChatGPT paid accounts in this BrowserOS workflow is:

- First subscribe to the cheapest paid personal plan.
- Then upgrade that already-paid account to the target personal Pro tier.
- Do not skip straight from Free to the expensive Pro tier.

Observed Pro upgrade path for `pro6@fun.country`:

- Start from the confirmed `Pro Six Go` account.
- Open profile menu -> `Upgrade plan`.
- If the plan modal is on `Business`, switch back to `Personal`.
- In the personal Pro card, select `20x`.
- Confirm the Pro card shows `$200 USD / month`.
- Click `Upgrade to Pro`.
- In the confirmation modal, click `Pay now`.

Observed final charge modal:

- `ChatGPT Pro subscription`: `$200.00`
- Go plan prorated credit: `-$8.00`
- Subtotal: `$192.00`
- Tax: `$12.29`
- Total due today: `$204.29`
- Payment method: saved Visa ending `9278`

Successful result:

- After payment, the Pro card showed `Your current plan`.
- The page initially kept a stale `Go` profile label.
- Reloading ChatGPT refreshed the profile menu to `Pro Six Pro`.

## 2026-05-02 - AIM Manual Codex OAuth For `pro6`

For a new Codex/ChatGPT account that is already signed into BrowserOS, run the
AIM OAuth flow locally. The browser side depends on the local BrowserOS profile,
so do not try to complete the browser step on `agents@amirs-mac-studio`.

Confirmed local browser identity:

- BrowserOS `browserContextId` `Profile 1` maps to profile display name `pro6`.
- `Profile 1` is signed into `pro6@fun.country`.

Local AIM setup:

```bash
rtk aim browser set pro6 --mode manual-callback
rtk aim login pro6
```

Observed `aim login pro6` behavior:

- AIM attempted to bind `http://127.0.0.1:1455`.
- That port was already in use during this run, so AIM fell back to the manual
  paste flow.
- AIM printed an OpenAI OAuth URL.
- Opening that URL in BrowserOS `Profile 1` reached the OpenAI Codex consent
  page.
- Clicking `Continue` redirected to a `http://localhost:1455/auth/callback?...`
  URL.
- Pasting the full callback URL back into the waiting local `aim login pro6`
  prompt completed auth and stored fresh `openai-codex` credentials.

Post-auth local metadata set for the label:

```json
{
  "provider": "openai-codex",
  "expect": {
    "email": "pro6@fun.country"
  },
  "reauth": {
    "mode": "manual-callback"
  },
  "pool": {
    "enabled": true
  },
  "browser": null
}
```

Publish note:

- Current `aim promote codex --to ... <label>` is an update path for labels
  that were already imported from the same authority.
- A brand-new local label such as `pro6` is not promotable through that command
  until it exists on the authority.
- For this first publish, merge only `accounts.pro6` and
  `credentials.openai-codex.pro6` into the remote AIM state, with a remote
  backup, then sync local AIM from the authority.

Commands used after local auth:

```bash
rtk aim sync codex --from agents@amirs-mac-studio
```

Remote publish result:

- Remote AIM state path: `/Users/agents/.aimgr/secrets.json`
- Remote backup created:
  `/Users/agents/.aimgr/secrets.json.bak.2026-05-02T18-40-06-452Z`
- Remote `pro6` provider: `openai-codex`
- Remote `pro6` reauth mode: `manual-callback`
- Remote `pro6` pool enabled: `true`
- Local post-sync import source: `agents@amirs-mac-studio`
- Local post-sync `pro6` import dirty flag: `false`

Do not touch OpenClaw for this workflow:

- Do not run `aim rebalance openclaw`.
- Do not run `aim apply`.
- Do not change OpenClaw assignments as part of adding a new Codex account to
  AIM.

Secret-handling rule:

- Do not write OAuth access tokens, refresh tokens, ID tokens, callback codes,
  or full callback URLs into notes or chat.

## 2026-05-02 - Full `pro6` Bring-Up Runbook

This is the repeatable end-to-end process used for `pro6`, from BrowserOS
profile ownership through ChatGPT payment and AIM Codex pool publication.

Safety rules for the whole run:

- Do not print or save Google passwords, Ramp card numbers, CVCs, OAuth tokens,
  ID tokens, refresh tokens, callback codes, or full callback URLs in notes.
- Use secret files as data. Do not shell-source password files when the value
  can contain shell-special characters.
- Keep the first ChatGPT paid checkout and the later Pro upgrade as two
  separate purchase decisions.
- Do not touch OpenClaw when the task is only "add a new Codex account to AIM
  rotation."

BrowserOS profile grounding:

```bash
rtk jq -r '.profile.info_cache | to_entries[] | "\(.key)\t\(.value.name)"' \
  "/Users/aelaguiz/Library/Application Support/BrowserOS/Local State"
```

Observed mapping:

```text
Default    Work
Profile 1 pro6
```

Use profile contexts this way:

- `Profile 1` / `pro6`: Google, Gmail, ChatGPT, OpenAI OAuth for `pro6`.
- `Default` / `Work`: Ramp and admin/work accounts.

BrowserOS/CDP rule:

- BrowserOS MCP snapshots/clicks/fills work for many app controls.
- Google and Stripe secure inputs may ignore ordinary paste/fill.
- When an input looks empty after paste, focus the exact field and send text
  through CDP `Input.insertText`, one character at a time for Stripe card
  fields.

Google/Gmail account setup:

- Go to `mail.google.com` in BrowserOS `Profile 1`.
- Sign in as `pro6@fun.country`.
- If Google forces a password change, fill both password fields using focused
  browser input/CDP and save the real password under `~/workspace/secrets`.
- Confirm success by reaching:

```text
https://mail.google.com/mail/u/0/#inbox
```

ChatGPT signup:

- In BrowserOS `Profile 1`, search Google for `chatgpt`.
- Click through to `chatgpt.com`.
- Submit a small public test prompt while logged out.
- Click `Sign up for free`.
- Choose `Continue with Google`.
- Pick the already logged-in `pro6@fun.country` account.
- Complete profile/onboarding.
- Confirm the signed-in ChatGPT page shows the `Pro Six` account.

Ramp card creation:

- In BrowserOS `Default`, use the live Ramp tab.
- Go to `Manage spend` -> `Cards`.
- Click `Issue`.
- Choose `Product or service`.
- Set product/vendor to `OpenAI`.
- Set limit to `$250`.
- Set cadence to `Monthly`.
- Issue the virtual card.
- Rename the card to match the existing convention:

```text
Pro - Pro6
```

Ramp card/address handling:

- Use Ramp's secure copy controls for card number, expiration, CVC, billing
  name, and billing address pieces.
- Do not log the copied payment values.
- For ChatGPT/Stripe card fields, focus each secure field and type copied card
  values character-by-character if paste does not populate the field.

ChatGPT paid plan process:

- Always subscribe to the cheapest paid personal plan first.
- Then upgrade that paid account to the target personal Pro tier.
- Do not skip straight from Free to the expensive Pro tier.

Observed `pro6` paid path:

- First checkout: ChatGPT Go at `$8.00/month`.
- Billing address selection added sales tax and made due-today total `$8.51`.
- After subscription, the profile menu showed `Pro Six Go`.
- Upgrade path: profile menu -> `Upgrade plan` -> switch to `Personal` if the
  modal opens on `Business` -> choose personal Pro `20x` -> confirm
  `$200 USD / month` -> `Upgrade to Pro` -> `Pay now`.
- Observed Pro upgrade modal:
  - ChatGPT Pro subscription: `$200.00`
  - Go credit: `-$8.00`
  - Subtotal: `$192.00`
  - Tax: `$12.29`
  - Total due today: `$204.29`
- After payment, reload ChatGPT if the profile label is stale.
- Final observed account label: `Pro Six Pro`.

AIM local manual OAuth:

Run this locally, not on `agents@amirs-mac-studio`, because the browser profile
that can complete OAuth is local BrowserOS `Profile 1`.

```bash
rtk aim browser set pro6 --mode manual-callback
rtk aim login pro6
```

During this run:

- AIM tried to bind `http://127.0.0.1:1455`.
- The port was already in use, so AIM printed an OAuth URL and used manual
  callback paste.
- Open the OAuth URL in BrowserOS `Profile 1`.
- The OpenAI Codex consent page appears.
- Click `Continue`.
- BrowserOS lands on a `http://localhost:1455/auth/callback?...` page.
- Copy the full callback URL from the address bar.
- Paste it into the waiting local `aim login pro6` terminal prompt.
- AIM returns `ok: true` with provider `openai-codex` and maintenance status
  `ready`.
- Close the callback tab after use because it contains a one-time OAuth code.

Set/confirm local AIM metadata:

```bash
rtk node --input-type=module -e '
import { loadAimgrState } from "./src/state/schema.js";
import { writeJsonFileWithBackup } from "./src/io/json-store.js";
const statePath = `${process.env.HOME}/.aimgr/secrets.json`;
const state = loadAimgrState(statePath);
const label = "pro6";
state.accounts[label] ??= {};
state.accounts[label].provider = "openai-codex";
state.accounts[label].expect = {
  ...(state.accounts[label].expect || {}),
  email: "pro6@fun.country",
};
state.accounts[label].reauth = {
  ...(state.accounts[label].reauth || {}),
  mode: "manual-callback",
};
state.accounts[label].pool = {
  ...(state.accounts[label].pool || {}),
  enabled: true,
};
state.accounts[label].browser = null;
writeJsonFileWithBackup(statePath, state);
const c = state.credentials?.["openai-codex"]?.[label];
console.log(JSON.stringify({
  ok: true,
  label,
  provider: state.accounts[label].provider,
  email: state.accounts[label].expect.email,
  reauth: state.accounts[label].reauth.mode,
  pool: state.accounts[label].pool.enabled !== false,
  hasCredential: !!c,
  expiresAt: c?.expiresAt ?? null,
}, null, 2));
'
```

Expected local state shape:

```json
{
  "provider": "openai-codex",
  "expect": {
    "email": "pro6@fun.country"
  },
  "browser": null,
  "reauth": {
    "mode": "manual-callback"
  },
  "pool": {
    "enabled": true
  }
}
```

Local verification without tokens:

```bash
rtk node -e 'const fs=require("fs"); const s=JSON.parse(fs.readFileSync(process.env.HOME+"/.aimgr/secrets.json","utf8")); const a=s.accounts.pro6; const c=s.credentials["openai-codex"].pro6; console.log(JSON.stringify({label:"pro6",provider:a?.provider,expectEmail:a?.expect?.email,reauth:a?.reauth?.mode,pool:a?.pool?.enabled!==false,hasCredential:!!c,expiresAt:c?.expiresAt},null,2));'
```

Observed local credential expiry after auth:

```text
2026-05-12T18:39:15.629Z
```

Optional token-claim verification:

- Decode only non-secret JWT claims.
- For this run, the token claim showed ChatGPT plan type `pro`.
- Do not print the token itself.

First publish to `agents@amirs-mac-studio`:

- `aim promote codex --to agents@amirs-mac-studio pro6` is not the first-publish
  path for a brand-new label.
- The current promote command only updates labels already imported from that
  same authority.
- For a brand-new local label, first seed only that one label into the remote
  AIM state:
  - `accounts.pro6`
  - `credentials.openai-codex.pro6`
- Back up the remote state before replacing it.
- Refuse to overwrite a remote `pro6` with a different provider or account id.
- Do not copy local target state, OpenClaw assignments, Codex active target, or
  any machine-local state to the remote.

The first publish used an SSH stdin payload with this shape:

```json
{
  "kind": "aimgr.oneLabelCodexSeed.v1",
  "label": "pro6",
  "account": {
    "provider": "openai-codex",
    "expect": {
      "email": "pro6@fun.country"
    },
    "reauth": {
      "mode": "manual-callback"
    },
    "pool": {
      "enabled": true
    },
    "browser": null
  },
  "credential": "<local credentials.openai-codex.pro6 object, not logged>"
}
```

Remote write invariants:

- Remote path: `/Users/agents/.aimgr/secrets.json`
- Backup path pattern:

```text
/Users/agents/.aimgr/secrets.json.bak.<timestamp>
```

- This run created:

```text
/Users/agents/.aimgr/secrets.json.bak.2026-05-02T18-40-06-452Z
```

Post-publish sync:

```bash
rtk aim sync codex --from agents@amirs-mac-studio
```

Observed import result included `pro6` in `importedLabels` and no removed
labels.

Final local verification:

```bash
rtk node -e 'const fs=require("fs"); const s=JSON.parse(fs.readFileSync(process.env.HOME+"/.aimgr/secrets.json","utf8")); const a=s.accounts.pro6; const c=s.credentials["openai-codex"].pro6; const m=s.imports.authority.codex.labelsByName.pro6; console.log(JSON.stringify({label:"pro6",provider:a?.provider,expectEmail:a?.expect?.email,reauth:a?.reauth?.mode,pool:a?.pool?.enabled!==false,hasCredential:!!c,expiresAt:c?.expiresAt,imported:!!m,dirty:!!m?.dirtyLocal,source:s.imports.authority.codex.source},null,2));'
```

Expected final local facts:

```text
label: pro6
provider: openai-codex
expectEmail: pro6@fun.country
reauth: manual-callback
pool: true
hasCredential: true
expiresAt: 2026-05-12T18:39:15.629Z
imported: true
dirty: false
source: agents@amirs-mac-studio
```

Final remote verification:

```bash
rtk ssh agents@amirs-mac-studio 'node -e '\''const fs=require("fs"); const s=JSON.parse(fs.readFileSync(process.env.HOME+"/.aimgr/secrets.json","utf8")); const a=s.accounts.pro6; const c=s.credentials["openai-codex"].pro6; console.log(JSON.stringify({label:"pro6",provider:a&&a.provider,expectEmail:a&&a.expect&&a.expect.email,reauth:a&&a.reauth&&a.reauth.mode,pool:!a.pool||a.pool.enabled!==false,hasCredential:!!c,expiresAt:c&&c.expiresAt},null,2));'\'''
```

Expected final remote facts:

```text
label: pro6
provider: openai-codex
expectEmail: pro6@fun.country
reauth: manual-callback
pool: true
hasCredential: true
expiresAt: 2026-05-12T18:39:15.629Z
```

OpenClaw non-action verification:

- This workflow must not run OpenClaw commands.
- After the remote one-label publish, remote OpenClaw timestamps were still:

```text
openclawLastRebalancedAt: 2026-03-28T20:47:55.330Z
openclawLastApplyObservedAt: 2026-03-28T20:47:55.330Z
```

Future refresh path:

- Once `pro6` exists on the authority and local AIM has synced it back, future
  local refreshes should use the normal imported-label path:

```bash
rtk aim login pro6
rtk aim promote codex --to agents@amirs-mac-studio pro6
rtk aim sync codex --from agents@amirs-mac-studio
```

- Only use the one-label seed merge for the first publish of a brand-new label
  that does not yet exist on the authority.
