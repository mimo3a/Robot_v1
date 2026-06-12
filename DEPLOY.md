# Deploy to Raspberry Pi

GitHub Actions deploys the project to Raspberry Pi over SSH after every push to
the `speed_manage` branch.

## Required GitHub Secrets

Set these in GitHub:

`Settings -> Secrets and variables -> Actions -> New repository secret`

- `PI_HOST`: Raspberry Pi IP address or hostname, for example `192.168.1.25`
- `PI_USER`: Raspberry Pi SSH user, for example `pirobot`
- `PI_SSH_KEY`: private SSH key that can log in to the Pi

Optional secrets:

- `PI_PORT`: SSH port. Default is `22`
- `PI_DEPLOY_PATH`: target folder on the Pi. Default is `/home/pirobot/robot`
- `PI_SERVICE_NAME`: systemd service to restart after deploy, for example
  `robot.service`

## Create SSH Key

On your computer:

```bash
ssh-keygen -t ed25519 -C "github-actions-robot" -f github_actions_robot
```

Copy the public key to the Pi:

```bash
ssh-copy-id -i github_actions_robot.pub pirobot@PI_HOST
```

Put the private key content from `github_actions_robot` into the GitHub secret
`PI_SSH_KEY`.

## Manual Deploy

Open GitHub Actions, choose `Deploy to Raspberry Pi`, then click
`Run workflow`.
