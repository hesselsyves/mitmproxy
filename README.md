# Installation (linux & WSL)

Download and unzip https://downloads.mitmproxy.org/12.2.0/mitmproxy-12.2.0-linux-x86_64.tar.gz

Run it in your terminal

```
./mitmproxy --listen-host 0.0.0.0 --listen-port 8888 --ssl-insecure --set anticomp=true
```

Run the webui:
```
./mitmweb --listen-host 0.0.0.0 --listen-port 8888 --ssl-insecure --set anticomp=true
```

Open the options and make sure you enable these checkboxes:

- Don't verify server certificates 
- anticomp
Try to convince servers to send us un-compressed data.

If you don't check anticomp, disable gzip on the source.

- create .ddev/nginx/nginx-site.conf with:

```
# Disable compression in nginx for correct ETag headers while using Charles Proxy.
# ETag behavior explanation:
# When requests are made directly from the Drupal client, Nginx returns a strong ETag because the response is uncompressed.
# When requests are routed through Charles Proxy or tools like Postman, even without header modification,
# Nginx may apply gzip compression based on default behavior or client headers (e.g., TE, User-Agent).
# This alters the response body, and Nginx marks the ETag as weak (W/...) to reflect that.
# To ensure consistent strong ETags, gzip compression was disabled in the DDEV Nginx config.
gzip off;

```
## Client setup (ddev)

- Create the dockerFile:
.ddev/web-build/Dockerfile.proxy

- Copy the certificate from ~/.mitmproxy/mitmproxy-ca-cert.pem next to your dockerfile

- Add this in the dockerfile
```
COPY mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
COPY charles.pem /usr/local/share/ca-certificates/charles.crt
RUN update-ca-certificates --fresh
```

- rebuild ddev

```
ddev debug rebuild
```

- Update ClientFactory.php

```
public function createClient(string $configName, array $clientConfig = []): Client {
    $config = $this->configFactory->get($configName);

    $prepared_config = $this->prepareClientConfig($config, $clientConfig);

	// This is new:
    $prepared_config['proxy'] = 'host.docker.internal:8888';

    return new Client(
      $prepared_config
    );
  }
```

- update CommonClientConfigurationTrait.php

```
function prepareCommonConfiguration(ImmutableConfig $config, array $clientConfig = []): array {
    $prepared_config = $clientConfig;

    $defaults = [
      RequestOptions::TIMEOUT => $clientConfig[RequestOptions::TIMEOUT] ?? 10,
      RequestOptions::CONNECT_TIMEOUT => $clientConfig[RequestOptions::TIMEOUT] ?? 10,
    ];

    foreach (array_keys($defaults) as $option) {
      $prepared_config[$option] = $config->get($option) ?? $defaults[$option];
    }

	// This is new:
    if (!is_null($config->get(RequestOptions::PROXY))) {
      $prepared_config[RequestOptions::PROXY] = $config->get(RequestOptions::PROXY);
    }

    return $prepared_config;
  }
```

- Update config

```
$config['pnp_client.api']['base_uri'] = 'https://pnp-api.ddev.site/';
$config['pnp_client_api']['proxy'] = 'host.docker.internal:8888';

$config['crd_api_client.client']['base_uri'] = 'https://centraal-request-database.ddev.site/api/v1/';
$config['crd_api_client.client']['proxy'] = 'host.docker.internal:8888';

```


