# Logins, SSO, and OAuth

Read before running a command-line login, driving a sign-in page, or working
a gate. `SKILL.md` owns the rules; this file owns the mechanics.

## Contents

- Read a sign-in page as profile evidence
- Get into `Work`
- Command-line logins
- Site sign-in shapes
- A tab you did not open
- Callback pages and proof
- Gates: work them yourself
- Telling the user
- Worked examples

## Read a sign-in page as profile evidence

Each neo profile is its own cookie jar. `Work` (`Default`) holds the user's
Google accounts and their logins to the business consoles. Each `pro`
profile holds one ChatGPT login and that profile's own consultation Google
account, and nothing else.

Google's "Choose an account" page lists exactly the accounts signed into the
profile the page is in. Read it as a profile check:

| The chooser shows | It means | Do |
| --- | --- | --- |
| a single consultation account named for a `pro` profile | the page is in a `pro` profile | close your page, rebind to `Work`, open the site there |
| the user's own accounts (personal and company addresses) | the page is in `Work` | pick the account the site's workspace belongs to |
| the account you need marked "Signed out" | `Work`, but that Google session lapsed | sign it back in yourself (see "Gates") |

A site's own login wall reads the same way: a console the user works in
daily does not ask `Work` to log in. If it asks, run `browser_target` `get`
first, and only then treat the wall as real.

Which of the user's accounts a site uses is usually in the task notes, the
request, or the site's workspace name. When two accounts fit and nothing
says which, pick the one whose domain matches the site's workspace and
switch if the site rejects it. "Use another account" is for an account the
chooser does not list; use it only when the task names that account.

## Get into `Work`

`browser_target` `action="clear"` returns the session to `Work`; `set` with
`name="Work"` does the same explicitly. `get` confirms `Work` and directory
`Default`. Then `browser.open(url)` opens the site in a background tab of a
`Work` window. Rebind between calls, never inside `run`. If the task goes
back to ChatGPT afterwards, rebind to the consultation profile and `get`
again.

## Command-line logins

`gcloud`, `gh`, `aws`, `gws`, `vercel`, `firebase`, and similar tools "open
the browser" by handing a URL to the operating system, which puts it in
whatever browser and window it likes. Do not let that happen.

1. Read the tool's `--help` for a no-browser, device-code, or headless
   option and use it: `gcloud auth login --no-launch-browser`,
   `aws login --no-browser`, `gh auth login` without `--web`,
   `az login --use-device-code`.
2. Without one, run the tool with `BROWSER=true`. Tools that honor `BROWSER`
   run `true` instead of a browser, and the URL stays in the tool's output.
   Capture that output to a private file in the task folder; the URL carries
   a state token, so keep it out of notes, commits, and replies.
3. Bind to `Work` and open the URL with `browser.open` inside one `run`, so
   the URL is read from the file and never printed.
4. Drive the chooser and consent: choose the account, click Continue or
   Allow, and read each screen before acting.
5. Feed the tool what it needs: many flows redirect to `localhost:<port>`
   and the tool finishes on its own; code flows show a code to paste into
   the tool's stdin. Never read, log, or keep the callback URL's query.
6. Prove the login from the tool (`gcloud auth list`, `gh auth status`,
   `aws sts get-caller-identity`, or the read the task needs). "You may
   close this window" is not proof.
7. List your pages and close the sign-in page once the tool has proved the
   login. A second sign-in tab you did not open means the tool launched a
   browser anyway; report it with where it landed.

## Site sign-in shapes

"Continue with Google" on a site in `Work` does one of three things. List
pages after the click (`browser.pages.list()`, filtered by the provider's
host and yours):

- **Same tab.** Your page now shows the chooser. Continue there.
- **Popup.** Neo does not admit popup windows: a call on one returns
  `page_out_of_scope`, and it will not appear in your listing. Look for the
  site's redirect sign-in instead (many sites offer one under "other ways"
  or fall back to it), or open the site's sign-in URL directly in your own
  tab. If only the popup works, that step goes to the user, once, with the
  profile and tab title.
- **A page somewhere you did not choose.** Something launched a browser
  (next section). Do not use it.

Never open the chooser URL again "to see where it goes": each wrong open is
another login page the user has to notice.

## A tab you did not open

A sign-in tab that appears without your `browser.open` came from a browser
launch you did not prevent, or from the user, and it reads as `user` or
`other-agent`. If timing and the tool's OAuth host tie it to your own
command-line launch, handle it as the command-line section says. Otherwise
it is someone else's: name it and its profile in your report and do not
drive it. Close it only when it is plainly the flow you just finished.

## Callback pages and proof

An OAuth callback (`localhost:<port>`, `/oauth2/idpresponse`, `/callback`)
carries a code in its query string. Do not read, screenshot, quote, or keep
that URL; keep only origin and path. Prove consumption from the application
(the tool's status command, or the site showing the signed-in workspace),
then close the callback page. A callback that never redirects usually means
the tool stopped listening; check its output before opening anything else.

## Gates: work them yourself

A gate in `Work` is part of the task. Stopping at one costs the user a
context switch for something you could have finished.

- **Password prompt or a "Signed out" account.** `credentials`
  `action="list"` with the page shows the profile's saved logins for the
  site; `action="fill"` with a `credentialId` fills them without the
  password ever reaching you. Otherwise use a credential the task, the
  repo's notes, or the user's secrets files provide, entered with `act` and
  `sensitive: true` where neo cannot tell it is secret. Never put it in
  `run`, `evaluate_in_page`, the shell, notes, or replies.
- **"Verify it's you" or a code prompt.** Choose a method you can complete:
  a code sent to an inbox you can read, or an authenticator secret the user
  keeps for agents.
- **CAPTCHA.** Try it; a checkbox usually passes in the user's signed-in
  browser. Use a screenshot to see it.
- **Consent, terms, and account choosers.** Read and click through. A
  consent button that stays disabled may be waiting for page focus; see
  `profiles-and-focus.md`.
- **Workspace policy block ("This app is blocked").** Try the other account
  that fits. If every fitting account is blocked, report the block text and
  continue with work that does not need the site.

The user's step is only what needs their body or a secret only they hold: a
phone approval, a passkey or hardware key, a password stored nowhere you can
reach. Finish everything else first, then leave the page as it is, ask once
with the profile and tab title, and keep working on whatever does not depend
on it. `request_human_help` with that page and a short reason puts the
request in neo's cockpit; while it is waiting, do nothing on that page. When
the user is done, list pages and reread the page before acting.

## Telling the user

The user watches several windows and cannot tell which you mean. Name the
profile and the tab: "Google consent for gcloud, `Work` profile, background
tab 'Sign in - Google Accounts'." When you moved a site to another profile,
say from where to where. When you left a stray tab, say where it is.

## Worked examples

**A console after a ChatGPT consultation.** The user said "use pro1" for a
Pro review. Later the task needs a RudderStack change. RudderStack is not
ChatGPT, so: `browser_target` `clear`, `get` shows `Work`, then
`browser.open('https://app.rudderstack.com/')`. Opening it while still bound
to `pro1` produces `/login` and a chooser with only the consultation
account; the fix is to close that page and open the site in `Work`, not to
ask whether `Work` may be used.

**A CLI whose login "opens browser".** `gws auth login` has no no-browser
flag. Run it as `BROWSER=true gws auth login ... > <task folder>/gws-auth.log
2>&1` in the background, bind to `Work`, open the URL from the log in one
`run`, choose the user's company account, click Continue and Allow, then
prove it with `gws drive about get`.

**A page that is already signed in.** The task needs a PostHog read. Bound to
`Work`, the listing shows a PostHog tab owned by the user with the workspace
in its title. That proves the login. Open your own page on PostHog in `Work`,
which shares it; do not drive the user's tab, and do not ask them to log in.
