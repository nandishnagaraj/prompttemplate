import axios, { type AxiosInstance } from "axios";
import type { BitbucketPullRequest } from "./types.js";

let _cachedToken: string | null = null;
let _tokenExpiry = 0;

async function getOAuthToken(): Promise<string> {
  const clientId = process.env.BITBUCKET_CLIENT_ID;
  const clientSecret = process.env.BITBUCKET_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    throw new Error("BITBUCKET_CLIENT_ID and BITBUCKET_CLIENT_SECRET are required");
  }

  if (_cachedToken && Date.now() < _tokenExpiry) {
    return _cachedToken;
  }

  const response = await axios.post<{ access_token: string; expires_in?: number }>(
    "https://bitbucket.org/site/oauth2/access_token",
    new URLSearchParams({ 
      grant_type: "urn:bitbucket:oauth2:jwt",
      client_id: clientId,
      client_secret: clientSecret
    }),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      timeout: 15000
    }
  );

  _cachedToken = response.data.access_token;
  _tokenExpiry = Date.now() + ((response.data.expires_in ?? 3600) - 60) * 1000;
  return _cachedToken;
}

async function createClient(): Promise<AxiosInstance> {
  const baseURL = process.env.BITBUCKET_BASE_URL ?? "https://api.bitbucket.org/2.0";
  
  // Use repository access token if available (simpler)
  const repoToken = process.env.BITBUCKET_TOKEN;
  if (repoToken) {
    return axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        Authorization: `Bearer ${repoToken}`,
        Accept: "application/json"
      }
    });
  }
  
  // Fall back to OAuth
  const token = await getOAuthToken();

  return axios.create({
    baseURL,
    timeout: 30000,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/json"
    }
  });
}

export async function getPullRequest(workspace: string, repoSlug: string, prId: number): Promise<BitbucketPullRequest> {
  const client = await createClient();
  const { data } = await client.get<BitbucketPullRequest>(`/repositories/${workspace}/${repoSlug}/pullrequests/${prId}`);
  return data;
}

export async function getPullRequestDiff(workspace: string, repoSlug: string, prId: number): Promise<string> {
  const client = await createClient();
  const { data } = await client.get<string>(
    `/repositories/${workspace}/${repoSlug}/pullrequests/${prId}/diff`,
    {
      headers: {
        Accept: "text/plain"
      },
      responseType: "text"
    }
  );

  return typeof data === "string" ? data : String(data);
}

export async function createPullRequestComment(
  workspace: string,
  repoSlug: string,
  prId: number,
  rawText: string
): Promise<unknown> {
  const client = await createClient();
  const payload = {
    content: {
      raw: rawText
    }
  };

  const { data } = await client.post(`/repositories/${workspace}/${repoSlug}/pullrequests/${prId}/comments`, payload, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  return data;
}

export async function createInlinePullRequestComment(
  workspace: string,
  repoSlug: string,
  prId: number,
  rawText: string,
  filePath: string,
  line: number
): Promise<unknown> {
  const client = await createClient();
  const payload = {
    content: {
      raw: rawText
    },
    inline: {
      path: filePath,
      to: line
    }
  };

  const { data } = await client.post(`/repositories/${workspace}/${repoSlug}/pullrequests/${prId}/comments`, payload, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  return data;
}

export async function createCommitStatus(
  workspace: string,
  repoSlug: string,
  commitHash: string,
  state: "SUCCESSFUL" | "FAILED" | "INPROGRESS" | "STOPPED",
  key: string,
  name: string,
  description: string,
  url?: string
): Promise<unknown> {
  const client = await createClient();
  const payload = { key, state, name, description, url };

  const { data } = await client.post(`/repositories/${workspace}/${repoSlug}/commit/${commitHash}/statuses/build`, payload, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  return data;
}
