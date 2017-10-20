"A = avg(http.request_response.latency {server.pod_name ~ "sock-shop/catalogue"}) by ("http.uri","client.pod_name") top(10) offset 1h"
"A = avg(cpuUser) by ("instance.host_name")"
