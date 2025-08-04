import * as client from 'openid-client'

let server!: URL

let config: client.Configuration = await client.discovery(
	server,
)

let redirect_uri!: string
let scope!: string

let code_verifier: string = client.randomPKCECodeVerifier()
let code_challenge: string = await client.calculatePKCECodeChallenge(code_verifier)
let state!: string

let parameters: Record<string, string> = {
	redirect_uri,
	scope,
	code_challenge,
	code_challenge_method : 'S256',
}

if (!config.serverMetadata().supportsPKCE()) {
  state = client.randomState()
  parameters.state = state
}


