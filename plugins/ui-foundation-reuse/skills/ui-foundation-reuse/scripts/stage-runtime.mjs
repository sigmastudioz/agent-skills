// Copy the bundled runtime into an app; never download packages or rewrite its manifest.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const hash = value => crypto.createHash('sha256').update(value).digest('hex');

try {
  if (process.argv.length !== 3) throw Error('Usage: node stage-runtime.mjs <application-directory>');
  const project = fs.realpathSync(process.argv[2]);
  if (!fs.statSync(project).isDirectory() || !fs.existsSync(path.join(project, 'package.json'))) {
    throw Error('Choose an application directory containing package.json.');
  }
  const skill = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const metadata = JSON.parse(fs.readFileSync(path.join(skill, 'assets/bundle.json'), 'utf8'));
  if (metadata.package !== '@sigmastudioz/ui-foundation' || metadata.archive !== 'ui-foundation.tgz') {
    throw Error('Unexpected bundled runtime metadata.');
  }
  const bytes = fs.readFileSync(path.join(skill, 'assets', metadata.archive));
  if (hash(bytes) !== metadata.sha256) throw Error('Bundled archive checksum mismatch; obtain an intact skill copy.');

  // Keep all writes inside the chosen app, including when a vendor path is a symlink.
  let directory = project;
  for (const segment of ['vendor', 'ui-foundation']) {
    directory = path.join(directory, segment);
    let existing;
    try { existing = fs.lstatSync(directory); } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
    if (existing && (existing.isSymbolicLink() || !existing.isDirectory())) {
      throw Error(`Use a real directory for ${path.relative(project, directory)}; no files were replaced.`);
    }
    if (!existing) {
      fs.mkdirSync(directory);
    }
  }
  const relative = 'vendor/ui-foundation/ui-foundation.tgz';
  const target = path.join(project, relative);
  try {
    const existing = fs.lstatSync(target);
    if (!existing.isFile() || existing.isSymbolicLink() || hash(fs.readFileSync(target)) !== metadata.sha256) {
      throw Error('A different runtime already exists in vendor/ui-foundation; review and back it up before upgrading.');
    }
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    fs.writeFileSync(target, bytes, { flag: 'wx' });
  }
  console.log(JSON.stringify({
    package: metadata.package,
    version: metadata.version,
    archive: relative,
    sha256: metadata.sha256,
    dependency: `file:${relative}`,
    next: `Install ./${relative} using this application's package manager, then inspect the resolved exports and peer requirements.`,
  }, null, 2));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
