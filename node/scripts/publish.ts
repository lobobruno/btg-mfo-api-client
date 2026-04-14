#!/usr/bin/env tsx
import { execSync } from 'node:child_process';
import * as fs from 'node:fs';
import * as path from 'node:path';

function exec(
  command: string,
  options?: { stdio?: 'inherit' | 'pipe' }
): string {
  const result = execSync(command, {
    encoding: 'utf-8',
    stdio: options?.stdio ?? 'pipe',
  });
  return result?.trim() ?? '';
}

function getPackageJson(): {
  version: string;
  name: string;
  [key: string]: unknown;
} {
  const packagePath = path.join(process.cwd(), 'package.json');
  return JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
}

function savePackageJson(pkg: object): void {
  const packagePath = path.join(process.cwd(), 'package.json');
  fs.writeFileSync(packagePath, `${JSON.stringify(pkg, null, 2)}\n`);
}

function incrementVersion(version: string): string {
  const parts = version.split('.').map(Number);
  parts[parts.length - 1] += 1;
  return parts.join('.');
}

function parseArgs(): { version?: string } {
  const args = process.argv.slice(2);
  const versionIndex = args.indexOf('--version');

  if (versionIndex !== -1 && args[versionIndex + 1]) {
    return { version: args[versionIndex + 1] };
  }

  const versionArg = args.find((arg) => arg.startsWith('--version='));
  if (versionArg) {
    return { version: versionArg.split('=')[1] };
  }

  return {};
}

async function main(): Promise<void> {
  console.log('\n🚀 btg-mfo-api-client - Publish Script\n');
  console.log('─'.repeat(50));

  const { version: customVersion } = parseArgs();
  const pkg = getPackageJson();
  const currentVersion = pkg.version;

  let newVersion: string;
  if (customVersion) {
    if (!/^\d+\.\d+\.\d+(-[\w.]+)?$/.test(customVersion)) {
      console.log(
        '\n❌ Invalid version format. Use semver (e.g., 1.2.3 or 1.2.3-beta.1)\n'
      );
      process.exit(1);
    }
    newVersion = customVersion;
  } else {
    newVersion = incrementVersion(currentVersion);
  }

  console.log(`\n📦 Package: ${pkg.name}`);
  console.log(`📌 Current version: ${currentVersion}`);
  console.log(`📝 New version: ${newVersion}\n`);
  console.log('─'.repeat(50));

  try {
    console.log('\n🔍 Running lint...');
    exec('pnpm run lint', { stdio: 'inherit' });
    console.log('✅ Lint passed!\n');

    console.log('🔍 Running typecheck...');
    exec('pnpm run typecheck', { stdio: 'inherit' });
    console.log('✅ Typecheck passed!\n');

    console.log('🔨 Building...');
    exec('pnpm run build', { stdio: 'inherit' });
    console.log('✅ Build completed!\n');

    console.log('📝 Updating package.json version...');
    pkg.version = newVersion;
    savePackageJson(pkg);
    console.log(`✅ Version updated to ${newVersion}\n`);

    console.log('📦 Creating git commit...');
    exec('git add package.json');
    exec(
      `git commit -m ":bookmark: release btg-mfo-api-client v${newVersion}"`
    );
    console.log('✅ Commit created!\n');

    const tag = `btg-mfo-api-client-v${newVersion}`;
    console.log('🏷️  Creating git tag...');
    exec(`git tag -a ${tag} -m "Release btg-mfo-api-client v${newVersion}"`);
    console.log(`✅ Tag ${tag} created!\n`);

    console.log('⬆️  Pushing to remote...');
    exec('git push');
    exec('git push --tags');
    console.log('✅ Pushed to remote!\n');

    console.log('🚀 Publishing to npm...');
    exec('npm publish --access public', { stdio: 'inherit' });
    console.log('\n✅ Published to npm!\n');

    console.log('─'.repeat(50));
    console.log(`\n🎉 Successfully published ${pkg.name}@${newVersion}!\n`);
    console.log(`   npm: https://www.npmjs.com/package/${pkg.name}`);
    console.log(
      `   GitHub: https://github.com/lobobruno/btg-mfo-api-client/releases/tag/${tag}\n`
    );
  } catch (error) {
    console.error('\n❌ Error during publish:', error);
    console.log(
      '\n⚠️  You may need to manually revert changes if any were made.\n'
    );
    process.exit(1);
  }
}

main();
