export const ALLOWED_HOSTS = ['api.btgpactual.com'] as const;

export function buildBtgUrl(
  path: string,
  query?: Record<string, string>
): string {
  const url = new URL(path, `https://${ALLOWED_HOSTS[0]}`);

  if (!(ALLOWED_HOSTS as readonly string[]).includes(url.hostname)) {
    throw new Error(`Host "${url.hostname}" is not in the BTG allowlist`);
  }

  if (query) {
    for (const [key, value] of Object.entries(query)) {
      url.searchParams.set(key, value);
    }
  }

  return url.toString();
}
