Name:       __PACKAGE_NAME__
Version:    __SOFTWARE_VERSION__
Release:    __RELEASE_VERSION__
Summary:    __PACKAGE_DESC__

License:    __LICENSE__

Requires:   bash, python, nginx, python-daemon, python-flask, python-httplib2, python-requests, python-sqlalchemy, gunicorn, nodejs, npm

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


##############################################################################
# preun macro to run prior to uninstallation
##############################################################################
%preun

echo "Executing Pre-Uninstallation macro.. "

if [ $1 -gt 1 ] ; then
    # Upgrading already installed package
    echo -n "Restarting service..."
    systemctl daemon-reload
    systemctl start __PACKAGE_NAME__ || true
    echo " OK"
    echo ""
    echo "Service __PACKAGE_NAME__ upgraded successfully!!"

else
    # Performing a fresh install of  the package
    echo -n "Starting service..."
    systemctl daemon-reload
    systemctl enable __PACKAGE_NAME__ || true
    echo " OK"
    echo ""
    echo "Service __PACKAGE_NAME__ installed successfully!"
    echo ""
    echo "Edit the file __PACKAGE_DIR__/config/settings.cfg with your credentials, then start the service with the following:"
    echo "  systemctl start __PACKAGE_NAME__"

fi

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
%defattr(755,root,www-data)
/opt/
/etc/
%config(noreplace) __PACKAGE_DIR__/config/settings.cfg

%doc


##############################################################################
# changelog macro to comment on package revisions (date format important)
##############################################################################
%changelog
* Sat Jul 28 2018 zlig <noreply@gdevnet.com>
- Initial build

