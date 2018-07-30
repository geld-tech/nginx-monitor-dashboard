# nginx-monitor-dashboard

## Status

<table>
  <tr>
    <td colspan="2">Download</td>
    <td colspan="2"></td>
  </tr>
  <tr>
    <td>Ubuntu/Debian</td>
    <td>CentOS/Red Hat</td>
    <td>Build Status</td>
    <td>License</td>
  </tr>
  <tr>
    <td>
       [![Download](https://api.bintray.com/packages/geldtech/debian/nginx-monitor-dashboard/images/download.svg)](https://bintray.com/geldtech/debian/nginx-monitor-dashboard#files) 
    </td>
    <td>
        [![Download](https://api.bintray.com/packages/geldtech/rpm/nginx-monitor-dashboard/images/download.svg)](https://bintray.com/geldtech/rpm/nginx-monitor-dashboard#files)
    </td>
    <td>
        [![Build Status](https://travis-ci.org/geld-tech/nginx-monitor-dashboard.svg?branch=master)](https://travis-ci.org/geld-tech/nginx-monitor-dashboard)
    </td>
    <td>
        [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
    </td>
  </tr>
</table>


## Description
Dashboard displaying NGINX resources built with Python Flask, Vue.js, and Chart.js


## Demo

A sample demo of the project is hosted on <a href="http://geld.tech">geld.tech</a>.


## Install

### Ubuntu/Debian

* Install the repository information and associated GPG key (to ensure authenticity):
```
$ echo "deb https://dl.bintray.com/geldtech/debian /" | sudo tee -a /etc/apt/sources.list.d/geld-tech.list
$ sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com EA3E6BAEB37CF5E4
```

* Update repository list of available packages and clean already installed versions
```
$ sudo apt update
$ sudo apt clean
```

* Install package
```
$ sudo apt install nginx-monitor-dashboard
```

### CentOS/Red Hat

* Install the repository by creating the file /etc/yum.repos.d/zlig.repo:

```
echo "[geld.tech]
name=geld.tech
baseurl=https://dl.bintray.com/geldtech/rpm
gpgcheck=0
repo_gpgcheck=0
enabled=1" | sudo tee -a /etc/yum.repos.d/geld.tech.repo
```

* Install the package
```
sudo yum install nginx-monitor-dashboard
```


## Usage

* Reload services and start ours
```
$ sudo systemctl daemon-reload
$ sudo systemctl start nginx-monitor-dashboard
$ sudo systemctl status nginx-monitor-dashboard
```


## Development

Use `local-dev.sh` script to build and run locally the Flask server with API and the Vue web application with DevTools enabled for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/) and [Chrome](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd):

```
$ ./local-dev.sh
```
Then, access the application locally using a browser at the address: [http://0.0.0.0:5000/](http://0.0.0.0:5000/).

