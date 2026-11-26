# 6. Remote help

For the setup adult. Do this after [3-run-the-kit.md](3-run-the-kit.md). You use Tailscale and T3 Code. Only `$ADMIN` can connect. The kid has no network.

## 1. What you need

| Item | Where |
|---|---|
| Tailscale, Personal (free) plan | tailscale.com |
| Tailscale on your computer | Same account as the device |
| T3 Code on your computer | Installed on your computer |

## 2. Set up Tailscale (once)

1. On your computer, install Tailscale. Sign in with the **same account** as the device.
2. On the device, check that step e in [3-run-the-kit.md](3-run-the-kit.md) is done.
3. In the Tailscale admin console, open **Machines**. Select the device. Click **Disable key expiry**.
4. Open the tailnet policy file (**Access controls**).
5. Replace the default `check` SSH rule with this rule. Put in your `$ADMIN` name.

```json
"ssh": [{"action": "accept", "src": ["autogroup:member"], "dst": ["autogroup:self"], "users": ["$ADMIN"]}]
```

**Why:** `check` mode asks for a browser login often. T3 Code cannot answer that prompt.

**Why the same account:** `autogroup:self` works only when both devices share one login.

## 3. Add the device in T3 Code

1. On your computer, open T3 Code.
2. Choose **Settings**, then **Environments**, then **Add environment**.
3. Choose **SSH**.
4. Enter `$ADMIN@$HOST`.

**You should see:** the device in the environment list.

Check from a terminal on your computer:

```sh
ssh $ADMIN@$HOST true
```

**You should see:** no password prompt and no browser prompt.

## 4. What you can do remotely

| Task | How | Guide |
|---|---|---|
| Update the system | `sudo dnf upgrade --refresh` | [7-maintenance.md](7-maintenance.md) |
| Restart the device | `sudo reboot` | [7-maintenance.md](7-maintenance.md) |
| Add lessons and images | Run `library/build-library.sh` | [7-maintenance.md](7-maintenance.md) |
| Check failed services | `systemctl --failed` | [8-when-stuck.md](8-when-stuck.md) |
| Run an agent | Use T3 Code on the device as `$ADMIN` | — |

## 5. Safety

| Rule | Why |
|---|---|
| Only `$ADMIN` can use Tailscale SSH. | The kid's account cannot connect. |
| `$ADMIN` has no password login. | `install.sh` locks the password (step 9). Only Tailscale can connect. |
| The kid's account has no network. | `install.sh` blocks it with nftables (step 8). |
| The kid's account has no `sudo`. | The kid cannot change system files. |
| Keep key expiry off for this device only. | Access stops when the key expires. |
| Remove a lost device in Tailscale. | Open **Machines**, then select the device, then **Remove**. |

Do not share the root password or the `$ADMIN` password.

## Checklist

- [ ] Tailscale on the device and on your computer use the same account.
- [ ] Key expiry is off for the device.
- [ ] The policy rule uses `$ADMIN` only.
- [ ] `ssh $ADMIN@$HOST true` works with no prompt.
- [ ] T3 Code shows the device.
