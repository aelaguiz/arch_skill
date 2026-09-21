# Logins, SSO, and OAuth

Read before running a command-line login, driving a sign-in page, or working
a gate. `SKILL.md` owns the rules; this file owns the mechanics.

## Contents

- Read a sign-in page as profile evidence
- Command-line logins
- Site sign-in shapes and relisting
- A tab you did not open
- Callback pages and proof
- Gates: work them yourself
- Telling the user
- Worked examples

## Read a sign-in page as profile evidence

Each BrowserOS profile is its own cookie jar. `Work` (`Default`) holds the
user's Google accounts and the user's logins to the business consoles. Each
`pro` profile holds one ChatGPT login and one Google account,
`proN@fun.country`, and nothing else.

Google's "Choose an account" page lists exactly the accounts signed into the
profile the page is in. Read it as a profile check:

| The chooser shows | It means | Do |
| --- | --- | --- |
| only `Pro One pro1@fun.country` (or another single `proN`) | the page is in a `pro` profile | close your page, open the site in `Work` |
| the user's own accounts (a personal Gmail and their company addresses) | the page is in `Work` | pick the account the site's workspace belongs to |
| the account you need with "Signed out" next to it | `Work`, but that Google session lapsed | sign it back in yourself (see "Gates: work them yourself") |

The same reading applies to a site's own login wall: a console the user works
in daily does not ask `Work` to log in. If it asks, first prove which profile
the page is in with the check in `SKILL.md`, and only then treat the wall as
real.

Which of the user's accounts a site uses is usually in the task notes, the
request, or the site's workspace name. When two accounts both fit and the
notes do not say, pick the one whose domain matches the site's workspace and
switch if the site rejects it. "Use another account" is for an account the
chooser does not list; reach for it only when the task names that account.

## Command-line logins

`gcloud`, `gh`, `aws`, `gws`, `vercel`, `firebase`, and similar tools "open the
browser" by handing a URL to the operating system. BrowserOS is the default
handler, and it places the URL in the most recently active window, which is
whichever profile window the user touched last. Do not let that happen.

1. Read the tool's `--help` for a no-browser, device-code, or headless option
   and use it: `gcloud auth login --no-launch-browser` (prints a URL and then
   asks for a code), `aws login --no-browser`, `gh auth login` without `--web`
   (device flow with a one-time code), `az login --use-device-code`.
2. Without such an option, run the tool with `BROWSER=true` in its
   environment. Tools and libraries that honor `BROWSER` then run `true`
   instead of a browser, and the flow continues while the URL stays in the
   tool's output. Capture that output to a private file in the task folder;
   the URL carries a state token, so do not paste it into notes, commits, or
   the reply.
3. Take the URL from the output and open it in `Work` with `newPage` and the
   `Default` window ID. Run the profile check on the new page.
4. Drive the chooser and consent in that page: choose the account, click
   Continue or Allow, and read each screen before acting. React, Radix, and
   Google surfaces often ignore plain clicks in a background tab; dispatch the
   click through `evaluate` on the resolved element when `act` reports success
   without a change.
5. Feed the tool what it needs: many flows redirect to `localhost:<port>` and
   the tool finishes on its own; device and code flows show a code on the page
   that you paste into the tool's stdin. Never read, log, or persist the
   callback URL's query string.
6. Prove the login from the tool (`gcloud auth list`, `gh auth status`, `aws
   sts get-caller-identity`, or the read the task actually needs). A page that
   says "You may close this window" is not proof.
7. Relist. Close the sign-in page you opened once the tool has proved the
   login. If a second sign-in tab appeared that you did not open, the tool
   launched the browser anyway: report it as an orphan with its profile, and
   close it only if the relist proves it is the flow you just finished.

If the tool insists on launching the browser and prints no URL, let it launch,
then relist at once and find the new sign-in page by the tool's OAuth host. In
`Work`, drive it. Anywhere else, open the same URL in `Work` with `newPage`
inside one `run` call so the URL is never printed, finish there, and close the
stray page once the tool proves the login.

## Site sign-in shapes and relisting

Clicking "Continue with Google" on a site in `Work` produces one of three
shapes. Relist after the click, with the window map, to see which:

```js
const w = await browser.cdp('Browser.getWindows');
const dir = Object.fromEntries(w.windows.map(x => [x.windowId, x.browserContextId]));
const pages = await browser.pages.list();
return pages
  .filter(p => /accounts\.google\.com|<site host>/.test(p.url))
  .map(p => ({page: p.pageId, window: p.windowId, profileDir: dir[p.windowId],
              type: w.windows.find(x => x.windowId === p.windowId)?.windowType, title: p.title}));
```

- **Same tab.** The page you clicked now shows the chooser. Continue there.
- **Popup window.** A new window of type `popup` in the same profile holds the
  chooser; the original page waits. Work in the popup by its page ID; it
  closes itself on success. Relist again afterward and continue in the
  original page. Do not activate or resize the popup.
- **A page in a window you did not choose.** Something launched the browser
  (see the next section). Do not use it.

Never call `windows activate` to find the sign-in page, and never open the
chooser URL again "to see where it goes": each open in the wrong window is
another login page the user has to notice.

## A tab you did not open

A sign-in tab that appeared without your `newPage` call came from a browser
launch you did not prevent, or from the user. A page the relist ties to your
own tool launch, by timing and the tool's OAuth host, is task-caused: handle
it as the command-line section says. Otherwise treat it as user-owned under the
provenance table in `SKILL.md`: inventory it, name its profile in your report,
and do not drive it. If the relist proves it is the flow you just completed
through your own page, and it sits in a window this task controls, close it
and count it in the receipt; otherwise report it as unknown or orphan.

## Callback pages and proof

An OAuth callback (`localhost:<port>`, `/oauth2/idpresponse`, `/callback`)
carries a code in its query string. Do not read, screenshot, quote, or persist
that URL; keep only the origin and path. Prove consumption from the
originating application (the tool's status command, or the site now showing
the signed-in workspace), then close the callback page. A callback page that
never redirects usually means the tool stopped listening: check the tool's
output before opening anything else.

## Gates: work them yourself

A gate in `Work` is part of the task. Stopping at one costs the user a
context switch for something you could have finished, so try before you ask:

- **Password prompt or a "Signed out" account.** Click into the field and let
  the browser's saved password fill, then continue. Otherwise use a credential
  the task, the repo's notes, or the user's secrets files provide for this
  site. Enter it with `act`; never put it in `evaluate`, `run`, the shell,
  logs, notes, or the reply.
- **"Verify it's you" or a code prompt.** Choose the method you can complete:
  a code sent to an inbox you can read (the signed-in mail in `Work`, or a
  mail CLI), or an authenticator secret the user keeps for agents. Read the
  code, enter it, go on.
- **CAPTCHA.** Try it. A checkbox or a simple challenge usually passes in the
  user's own signed-in browser. Use a screenshot to see it, and take brief
  foreground only if the widget will not render in a background tab.
- **Consent, terms, and account choosers.** Read the screen and click through.
- **Workspace policy block ("This app is blocked").** Try the other account
  that fits the site. If every fitting account is blocked, report the exact
  block text and go on with work that does not need the site.

The user's step is only what needs their body or a secret only they hold: a
phone approval prompt, a passkey, fingerprint, or hardware key, a password
stored nowhere you can reach. Then finish everything else in the task first.
Leave the page as a background tab in `Work`, ask once with the profile and
tab title, and keep working on whatever does not depend on it. When they say
it is done, relist and reread the page before acting: they may have moved it
further than you expect. Read `profiles-and-focus.md` for the focus rules
around a step the user takes.

## Telling the user

The user watches several profile windows and cannot tell which one you mean.
Every mention of a login page, chooser, or consent screen names the profile
and the tab: "Google consent for gcloud, `Work` profile, background tab titled
'Sign in - Google Accounts'." When you moved a page, say where from and where
to. When you left a stray tab, say where it is.

## Worked examples

**A console after a ChatGPT consultation.** The user said "use pro1" for a Pro
review. Later the task needs a RudderStack allowlist change. RudderStack is not
ChatGPT, so it opens in `Work`: fresh window map, `newPage('https://app.rudderstack.com/', {background: true, windowId: <Default window>})`,
profile check on the new page, then the console. Opening it in the `pro1`
window instead produces `/login` and a chooser with only `pro1@fun.country`.
The right recovery is to close that page and open the site in `Work`, not to
ask whether `Work` may be used.

**A CLI whose login "opens browser".** `gws auth login` has no no-browser flag
but prints "Open this URL in your browser to authenticate". Run it as
`BROWSER=true gws auth login --scopes ... > <task folder>/gws-auth.log 2>&1`
in the background, read the URL from the log, open it in `Work` with
`newPage`, choose the user's company account, click Continue and Allow, then prove
with `gws drive about get`. Relist: if a second Google tab appeared anyway,
report it with its profile.

**A device flow.** `aws login --no-browser` prints an approval URL. Open it in
`Work` with `newPage`, approve as the signed-in console user, and prove with
`aws sts get-caller-identity`. The approval page can then be closed.

**A page that is already signed in.** The task needs a PostHog read. The relist
shows a PostHog page in `Work` with the workspace in its title. That page
proves the login: read it if the provenance rules let this task use it, or
open your own background page in the same `Work` window, which shares the
login. Do not ask the user to log in, and do not open the site anywhere else.
