Name:       __PACKAGE_NAME__
Version:    __SOFTWARE_VERSION__
Release:    __RELEASE_VERSION__
Summary:    __PACKAGE_DESC__

License:    __LICENSE__

Requires:   bash, python, epel-release, nginx, python-daemon, python-flask, python-httplib2, python-requests, python-sqlalchemy, python-gunicorn, nodejs, npm

##############################################################################
# description macro to include information in the RPM header
##############################################################################
%description
__PACKAGE_DESC__


##############################################################################
# install macro to prepare packaged files in the %{buildroot} directory
##############################################################################
%install

echo "Laying out the package's files and directories.. "
mkdir -p %{buildroot}
cp -rf %{package_files}/* %{buildroot}


##############################################################################
# pre macro to run before the install scripts run
##############################################################################
%pre

echo "Executing Pre-Installation macro.. "


##############################################################################
# post macro to execute after installation
##############################################################################
%post

echo "Executing Post-Installation macro.. "

if [ $1 -gt 1 ] ; then
    # Upgrading already installed package
    echo -n "Restarting service..."
    systemctl daemon-reload
    systemctl restart __PACKAGE_NAME__ || true
    systemctl restart __PACKAGE_NAME__-collector || true
    echo " OK"
    echo ""
    echo "Service __PACKAGE_NAME__ upgraded successfully!!"

else
    # Performing a fresh install of  the package
    echo -n "Installing service..."
    systemctl daemon-reload
    systemctl enable __PACKAGE_NAME__ || true
    systemctl enable __PACKAGE_NAME__-collector || true
    echo " OK"
    echo ""
    echo -n "Adding required user and group..."
    id -u www-data || useradd -MU www-data
    id -g www-data || usermod -L  www-data
    echo " OK"
    echo ""
    echo -n "Starting service..."
    systemctl start __PACKAGE_NAME__ || true
    systemctl start __PACKAGE_NAME__-collector || true
    echo " OK"
    echo ""
    echo "Service __PACKAGE_NAME__ installed successfully!"
    echo ""
    echo "Edit the file __PACKAGE_DIR__/config/settings.cfg with your credentials, then start the service with the following:"
    echo "  systemctl start __PACKAGE_NAME__"

fi


##############################################################################
# preun macro to run prior to uninstallation
##############################################################################
%preun

echo "Executing Pre-Uninstallation macro.. "

case "$1" in
  0)
    systemctl disable __PACKAGE_NAME__-collector || true
    systemctl stop __PACKAGE_NAME__-collector || true
    systemctl disable __PACKAGE_NAME__ || true
    systemctl stop __PACKAGE_NAME__ || true
    rm -f __PACKAGE_DIR__/config/settings.cfg
  ;;
  1)
    exit 0
  ;;
esac


##############################################################################
# postun to execute after uninstallation 
##############################################################################
%postun

echo "Executing Post-Uninstallation macro.. "


##############################################################################
# files macro defines what are the contents of the package
# 
# The files will be installed as the below structure on the target system
##############################################################################
%files
%defattr(755,root,www-data,775)
%dir __PACKAGE_DIR__
__PACKAGE_DIR__
/etc/systemd/system/*.service
/etc/geld/nginx.conf.d/__PACKAGE_NAME__.conf
/etc/nginx/conf.d/nginx-status.conf
%config(noreplace) __PACKAGE_DIR__/config/settings.cfg

%doc


##############################################################################
# changelog macro to comment on package revisions (date format important)
##############################################################################
%changelog
* Fri Apr 19 2019 zlig <noreply@gdevnet.com>
- Fixes date format
* Thu Feb 21 2019 zlig <noreply@gdevnet.com>
- Fixes order of macros
* Sat Jul 28 2018 zlig <noreply@gdevnet.com>
- Initial build

