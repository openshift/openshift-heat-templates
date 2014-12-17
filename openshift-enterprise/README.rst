==========================
OpenShift Enterprise templates
==========================

This directory contains files for deploying OpenShift Enterprise to an OpenStack environment via heat.

OpenShift Enteprise now requires that you use Red Hat Enterprise Linux 6.6, which can be downloaded from:
https://rhn.redhat.com/rhn/software/channel/downloads/Download.do?cid=16952

To build with diskimage-builder, do the following in the parent directory of enterprise-heat-templates::
  yum install diskimage-builder
  mkdir $HOME/tmp
  export ELEMENTS_PATH=heat-templates/openshift-enterprise/dib/elements
  export DIB_CLOUD_IMAGES=url rhel-guest-image-6-6.5-20131220.3-1.qcow2 image can be found (download this from rhn)

  # Either set the following variables if you have the packages in a yum repo
  # or specify an OpenShift Enterprise subscription pool id.

  # Use yum repos for package installation
  export DIB_CONF_JBOSS_REPO_BASE=<location of JBoss repo>
  export DIB_CONF_REPO_BASE=<location of OpenShift Enteprise repo>

  # Or, use Red Hat subscriptions for package installation
  export DIB_REG_TYPE=rhsm
  export DIB_RHSM_OSE_POOL=<OpenShift Enterprise subscription pool id>
  export DIB_RHSM_POOL=<Red Hat Enterprise Linux Server subscription pool id (if not setting a custom repo url for it)>

  # Or, Use Red Hat Network Satellite
  export DIB_REG_TYPE=rhn
  export DIB_SAT_URL=http://REDACTED/XMLRPC
  export DIB_SAT_CERT_RPM_URL=http://REDACTED/pub/rhn-org-trusted-ssl-cert-1.0-1.noarch.rpm
  export DIB_SAT_KEY=1-ose2-0 #Replace with your sat key.

  # You will need to provide credentials for the Red Hat Enterprise Linux
  # Server packages. If you don't provide a pool id with DIB_RHSM_POOL, a
  # matching subscription on your user account will be automatically attached to
  the system.
  export DIB_RHSM_USER=your_rhel_subscription_username
  export DIB_RHSM_PASSWORD=your_rhel_subscription_password

  # Add the following to the disk image bulding command:

  export DIB_OSE_VERSION=2.2
  export DIB_YUM_VALIDATOR_VERSION=2.2

  export TMP_DIR=$HOME/tmp
  export DIB_IMAGE_SIZE=5
  disk-image-create --no-tmpfs -a amd64 vm rhel openshift-enterprise-broker -o RHEL6-x86_64-broker

  export TMP_DIR=$HOME/tmp
  export DIB_IMAGE_SIZE=20
  disk-image-create --no-tmpfs -a amd64 vm rhel openshift-enterprise-node -o RHEL6-x86_64-node

  # If you encounter an error regarding insufficient disk space during the disk-image-create process, you should increase your disk space allocation by increasing the value of DIB_IMAGE_SIZE. The error message that indicates insufficient space will be similar to "installing package $package_name needs xMB on the / filesystem."

  # If you're not going to use disk-image-create to pre-install OpenShift Enterprise packages, make sure your image has enough diskspace to install the packages that the OpenShift Enterprise installer will need to install. Take a look here, http://docs.openstack.org/image-guide/content/ch_openstack_images.html.

  # Register the RHEL6-x86_64-broker and RHEL6-x86_64-node with OpenStack Glance::
  glance add name=RHEL6-x86_64-broker is_public=true disk_format=qcow2 container_format=bare < RHEL6-x86_64-broker.qcow2
  glance add name=RHEL6-x86_64-node is_public=true disk_format=qcow2 container_format=bare < RHEL6-x86_64-node.qcow2

Invoke Heat
-----------

Once you have the required disk images registered with glance, you can use OpenStack Heat to provision instances of your images and configure them to work together as an OpenShift infrastructure::

As an example, if you've installed the openshift-heat-templates rpm and you would like to use the OpenShift-1B1N-neutron.yaml template, you can run:

heat stack-create openshift --template-file=/usr/share/openshift-heat-templates/openshift-enterprise/heat/neutron/OpenShift-1B1N-neutron.yaml --parameters="key_name=${USER}_key;prefix=novalocal;broker_hostname=openshift.brokerinstance.novalocal;node_hostname=openshift.nodeinstance.novalocal;conf_install_method=rhsm;conf_sm_reg_name=username;conf_sm_reg_pass;conf_sm_reg_pool=OSE_pool_id;private_net_id=neturon_private_net_id;public_net_id=neutron_public_net_id;private_subnet_id=neutron_private_subnet_id;;yum_validator_version=2.2;ose_version=2.2"

If you're running the above from source, and you've cloned the openshift-heat-template git repo, just change the path to the OpenShift-1B1N-neutron.yaml accordingly.

Using Custom Yum repos
----------------------

By default, the Heat Orchestration Template assumes you're using the Yum installation method, which means it also expects you to pass parameters to heat for yum repositories. As an example, you can add the following to your list of parameters::

  conf_rhel_repo_base=http://example.com/rhel/server/6/6Server/x86_64/os;conf_jboss_repo_base=http://example.com/rhel/server/6/6Server/x86_64;conf_ose_repo_base=http://example.com/OpenShiftEnterprise/1.2/latest

Using Subscription Manager
--------------------------

You can switch from the default installation method by passing in the parameter conf_install_method, as demonstrated above. The allowed values, other than yum are rhsm and rhn. If you set the installation method to rhsm, you'll want to also pass in the following parameters conf_reg_sm_reg_name and conf_sm_reg_pass for the username and password respectively. Additionally, you'll need to set the conf_sm_reg_pool parameter with the value of the subscription pool id that corresponds to your OpenShift Enterprise subscription. When setting the conf_install_method to something other than yum it is not necessary to pass the conf_*_repo_base parameters::

  conf_install_method=rhsm;conf_sm_reg_name=myuser;cohnf_sm_reg_pass=mypass;conf_sm_reg_pool=XYZ01234567

Using RHN
---------

You can switch from the default installation method by passing in the parameter conf_install_method. The allowed values, other than yum are rhsm and rhn. If you set the installation method to rhn, you'll want to also pass in the following parameters conf_rhn_reg_name and conf_rhn_reg_pass for the username and password respectively. Additionally, you'll need to set the conf_rhn_reg_ak parameter with the value of the subscription activation key that corresponds to your OpenShift Enterprise subscription. The rhn installation method only works with RHN Satellite. When setting the conf_install_method to something other than yum it is not necessary to pass the conf_*_repo_base parameters::

  conf_install_method=rhn;conf_rhn_reg_name=myuser;conf_rhn_reg_pass=mypass;conf_rhn_reg_ak=activationkey

