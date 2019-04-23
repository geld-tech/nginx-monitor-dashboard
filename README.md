# nginx-monitor-dashboard

## Status

<table>
    <thead>
      <tr class="table">
        <th>Ubuntu/Debian</th>
        <th>CentOS/Red Hat</th>
        <th>Build Status</th>
        <th>License</th>
      </tr>
    </thead>
    <tbody class="odd">
      <tr>
        <td>
            <a href="https://bintray.com/geldtech/debian/nginx-monitor-dashboard#files">
                <img src="https://api.bintray.com/packages/geldtech/debian/nginx-monitor-dashboard/images/download.svg" alt="Download DEBs">
            </a>
        </td>
        <td>
            <a href="https://bintray.com/geldtech/rpm/nginx-monitor-dashboard#files">
                <img src="https://api.bintray.com/packages/geldtech/rpm/nginx-monitor-dashboard/images/download.svg" alt="Download RPMs">
            </a>
        </td>
        <td>
            <a href="https://travis-ci.org/geld-tech/nginx-monitor-dashboard">
                <img src="https://travis-ci.org/geld-tech/nginx-monitor-dashboard.svg?branch=master" alt="Build Status">
            </a>
        </td>
        <td>
            <a href="https://opensource.org/licenses/Apache-2.0">
                <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="">
            </a>
        </td>
      </tr>
    </tbody>
</table>


## Description
Dashboard displaying NGINX resources built with Python Flask, Vue.js, and Chart.js


## Demo

A sample demo of the project is hosted on <a href="http://geld.tech">geld.tech</a>.


## Install

### Ubuntu/Debian

* Install the repository information and associated GPG key (to ensure authenticity):
```
echo "deb https://dl.bintray.com/geldtech/debian /" | sudo tee -a /etc/apt/sources.list.d/geld-tech.list
apt-key adv --recv-keys --keyserver keyserver.ubuntu.com EA3E6BAEB37CF5E4
```

* Update repository list of available packages and clean already installed versions
```
apt update
apt clean
```

* Install package
```
apt install nginx-monitor-dashboard
```

### CentOS/Red Hat

* Install the repository by creating the file /etc/yum.repos.d/zlig.repo:

```
echo "[geld.tech]
name=geld.tech
baseurl=https://dl.bintray.com/geldtech/rpm
gpgcheck=0
repo_gpgcheck=0
enabled=1" | tee -a /etc/yum.repos.d/geld.tech.repo
```

* Install the package
```
yum install nginx-monitor-dashboard
```


## Usage

* Adds Google Analytics User Agent ID (optional)
  * Edit configuration file
  ```
  vim /opt/geld/webapps/nginx-monitor-dashboard/config/settings.cfg
  ```

  * Replace <GA_UA_ID> with own value
  ```
  [ganalytics]
  ua_id=<GA_UA_ID>
  ```

* Reload systemd services configuration and start nginx-monitor-dashboard service
```
systemctl daemon-reload
systemctl start nginx-monitor-dashboard
systemctl status nginx-monitor-dashboard
```


## Development

### Local Development

Use the Makefile targets from the provided Makefile to build and run locally the Flask server with API, a stub Nginx status, and the Vue web application with DevTools enabled for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/) and [Chrome](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd):

```
# Build application
make all

# Run application locally
make start
```
Then, access the application locally using a browser at the address: [http://0.0.0.0:5000/](http://0.0.0.0:5000/)

Type `make stop` at any stage to stop the local development application.


### Unit Tests

A series of unit tests is executable via a single command:

```
make tests
```


### Nginx Status Stub Daemon

A Nginx Status Stub service is running as a daemon to generate sample data locally when executing unit tests and during local develpment. It is accessible at the address: [http://0.0.0.0:8000/](http://0.0.0.0:8000/)

The `curl` command allows to fetch its output if needed:

```
curl http://0.0.0.0:8000/
  Active connections: 1
  server accepts handled requests
  1650 1650 9255
  Reading: 0 Writing: 2 Waiting: 3
```
