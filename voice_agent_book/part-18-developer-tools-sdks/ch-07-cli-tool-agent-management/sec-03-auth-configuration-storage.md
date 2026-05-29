# Section 03: Auth & Configuration Storage

## Overview

The CLI stores authentication credentials and configuration in a config file at `~/.config/voiceagent/.voiceagentrc`. Configuration follows a profile-based system supporting multiple environments. API keys are stored securely with optional system keyring integration for encrypted storage.

## Architecture

```
Configuration System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Config File Paths:
  Linux:   ~/.config/voiceagent/.voiceagentrc
  macOS:   ~/Library/Preferences/voiceagent/.voiceagentrc
  Windows: %APPDATA%/voiceagent/.voiceagentrc

Config Format (JSON):
{
  "profiles": {
    "default": {
      "api_key": "va_live_abc123",
      "environment": "production",
      "output": "table",
      "color": true
    },
    "sandbox": {
      "api_key": "va_test_xyz789",
      "environment": "sandbox",
      "output": "json",
      "color": true
    },
    "dev": {
      "api_key": "va_dev_local",
      "environment": "development",
      "output": "table"
    }
  },
  "current_profile": "default",
  "telemetry": true,
  "last_update_check": "2025-06-01T00:00:00Z"
}

Config Resolution Order (lowest to highest):
  1. Default values (hardcoded)
  2. Config file (.voiceagentrc)
  3. Environment variables (VOICE_AGENT_*)
  4. CLI flags (--api-key, --environment)

Secure Keyring Integration:
  If system keyring available:
    - Store api_key in system keyring
    - Store "keychain:my-key-name" in config file
  Fallback:
    - Store api_key directly in config file
    - File permissions: 600 (owner read/write only)
```

## Design Decisions

- **XDG Base Directory**: Config stored in XDG-compliant path (`~/.config/`)
- **Profile System**: Multiple profiles for different environments/accounts
- **System Keyring**: Optional OS-level encryption for API keys
- **Config Precedence**: CLI flags override env vars override config file

## Implementation Approach

```typescript
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

// Config file paths
function getConfigDir(): string {
  const xdg = process.env.XDG_CONFIG_HOME;
  if (xdg) return path.join(xdg, 'voiceagent');

  const home = os.homedir();
  if (process.platform === 'darwin') {
    return path.join(home, 'Library', 'Preferences', 'voiceagent');
  }
  if (process.platform === 'win32') {
    return path.join(process.env.APPDATA || '', 'voiceagent');
  }
  return path.join(home, '.config', 'voiceagent');
}

const CONFIG_PATH = path.join(getConfigDir(), '.voiceagentrc');

// Config schema
interface VoiceAgentConfig {
  profiles: Record<string, ProfileConfig>;
  current_profile: string;
  telemetry: boolean;
  last_update_check?: string;
}

interface ProfileConfig {
  api_key?: string;
  environment?: 'production' | 'sandbox' | 'development';
  output?: 'table' | 'json' | 'yaml';
  color?: boolean;
}

// Config manager
class ConfigManager {
  private config: VoiceAgentConfig;

  constructor() {
    this.config = this.load();
  }

  private load(): VoiceAgentConfig {
    try {
      if (fs.existsSync(CONFIG_PATH)) {
        const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
        return JSON.parse(raw);
      }
    } catch {
      // Invalid config — start fresh
    }

    return {
      profiles: {
        default: { environment: 'production', output: 'table' },
      },
      current_profile: 'default',
      telemetry: true,
    };
  }

  private save(): void {
    const dir = path.dirname(CONFIG_PATH);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    }
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(this.config, null, 2), {
      mode: 0o600,
    });
  }

  getProfile(name?: string): ProfileConfig {
    const profileName = name || this.config.current_profile;
    return this.config.profiles[profileName] || {};
  }

  setProfile(name: string, config: Partial<ProfileConfig>): void {
    this.config.profiles[name] = {
      ...this.config.profiles[name],
      ...config,
    };
    this.save();
  }

  getCurrentProfileName(): string {
    return this.config.current_profile;
  }

  setCurrentProfile(name: string): void {
    if (!this.config.profiles[name]) {
      throw new Error(`Profile '${name}' not found`);
    }
    this.config.current_profile = name;
    this.save();
  }

  async getApiKey(profileName?: string): Promise<string> {
    const profile = this.getProfile(profileName);
    const apiKey = profile.api_key;

    if (apiKey?.startsWith('keychain:')) {
      // Retrieve from system keychain
      const keychainName = apiKey.slice(9);
      return this.getFromKeychain(keychainName);
    }

    return apiKey || '';
  }

  async setApiKey(key: string, profileName?: string): Promise<void> {
    const name = profileName || this.config.current_profile;

    // Try system keychain first
    try {
      const keychainName = `voiceagent-${name}`;
      await this.storeInKeychain(keychainName, key);
      this.setProfile(name, { api_key: `keychain:${keychainName}` });
    } catch {
      // Fallback to config file storage
      this.setProfile(name, { api_key: key });
    }
  }

  private async storeInKeychain(name: string, value: string): Promise<void> {
    // Use keytar for system keychain
    const keytar = await import('keytar');
    await keytar.default.setPassword('voiceagent-cli', name, value);
  }

  private async getFromKeychain(name: string): Promise<string> {
    const keytar = await import('keytar');
    return (await keytar.default.getPassword('voiceagent-cli', name)) || '';
  }
}

// Config CLI commands
const configCommand = new Command('config')
  .description('Manage CLI configuration');

configCommand
  .command('set')
  .argument('<key>', 'Configuration key')
  .argument('<value>', 'Configuration value')
  .action(async (key, value) => {
    const config = new ConfigManager();
    config.setProfile(config.getCurrentProfileName(), { [key]: value });
    console.log(`Config updated: ${key}=${value}`);
  });

configCommand
  .command('profile')
  .command('create')
  .argument('<name>', 'Profile name')
  .action(async (name) => {
    const config = new ConfigManager();
    config.setProfile(name, {});
    console.log(`Profile '${name}' created`);
  });
```

## Integration Points

- **System Keyring**: keytar library for macOS Keychain, Linux Secret Service, Windows Credential Manager
- **Environment Variables**: `VOICE_AGENT_API_KEY`, `VOICE_AGENT_ENV`, `VOICE_AGENT_OUTPUT`
- **SDK Integration**: Config Manager provides API key to SDK client

## Production Considerations

- **File Permissions**: Config file stored with 600 permissions to protect API keys
- **Keyring Fallback**: Transparent fallback if system keyring is unavailable
- **Config Migration**: Migrate old config format on first run
- **Environment Variable Security**: Warn if API key is passed via command line (visible in process list)

## Open-Source Tools

- **keytar**: System keychain access for Node.js
- **env-paths**: Cross-platform config directory resolution
