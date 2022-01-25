#!/bin/bash
#   =====================================================================
# 
#	sap_monitor_hana_status.sh
#	Authored by			-	Jason Masipiquena
#						-	IBM - Lab for SAP Solutions
#
#	Bash script designed to be used as an Ansible module
#	Check status of SAP HANA system
#	Input: 	
#		- hana_sid
# 		- hana_instance_number
#	Output:
#		- GREEN YELLOW RED GRAY (based on the status from sapcontrol)
#		- Access the result from Ansible via <register_variable>.sap_status
#
#   =====================================================================

#   =====================================================================
#	Functions
#   =====================================================================
#	check_is_hdb_up
#	return_ansible

# Checks if SAP HANA system is up
function check_is_hdb_up(){
	# $1 - SIDADM
	# $2 - SID
	# $3 - NR
	local STATUS=$(su - $1 -c "sapcontrol -nr $3 -function GetSystemInstanceList | grep HDB")
	STATUS=$(echo $STATUS | awk '{ print $7 }')
	echo $STATUS
}


# Return values for Ansible
function return_ansible(){

	local result=$1

	if [ $result = "success" ]; then
		printf '{"changed": %s, "failed": %s, "msg": "%s", "sap_status": "%s"}' \
			false false "SAP Check $RETURN_MESSAGE" "$STATUS"
	else
		printf '{"changed": %s, "failed": %s, "msg": "%s", "sap_status": "%s"}' \
			false true "SAP Check Failed" "$STATUS"
	fi

	exit

}


#   =====================================================================
#	Main
#   =====================================================================
main () {

	export RETURN_MESSAGE="Successful"

	# These values are from Ansible
	export SID=$(echo ${hana_sid})
	export NR=$(echo ${hana_instance_number})

	export SIDADM=$(echo ${SID,,}adm)
	export HOSTNAME=$(uname -n)

	export STATUS=$(check_is_hdb_up $SIDADM $SID $NR)

	return_ansible success

}

# For Ansible module, source $1 will take all the input parameters
source $1
main
