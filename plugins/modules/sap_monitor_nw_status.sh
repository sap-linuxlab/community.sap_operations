#!/bin/bash
#   =====================================================================
# 
#	sap_monitor_nw_status.sh
#	Authored by			-	Jason Masipiquena
#						-	IBM - Lab for SAP Solutions
#
#	Bash script designed to be used as an Ansible module
#	Check status of SAP NW system
#	Input: 	
#		- nw_sid
# 		- nw_instance_number
#		- nw_instance_type
#	Output:
#		- GREEN YELLOW RED GRAY (based on the status from sapcontrol)
#		- Access the result from Ansible via <register_variable>.sap_status
#
#   =====================================================================

#   =====================================================================
#	Functions
#   =====================================================================
#	check_is_nw_up
#	return_ansible

# Checks if SAP NW system is up
function check_is_nw_up(){
	# $1 - SIDADM
	# $2 - NR
	# $3 - Type of instance
	INS_TYPE=$3
	INS_GREP=""

	if [[ $INS_TYPE = "PAS" ]]; then
		INS_GREP="ABAP"
	elif [[ $INS_TYPE = "ASCS" ]]; then
		INS_GREP="MESSAGE"
	elif [[ $INS_TYPE = "WebDisp" ]]; then
		INS_GREP="WEBDISP"
	elif [[ $INS_TYPE = "Java" ]]; then
		INS_GREP="J2EE"
	elif [[ $INS_TYPE = "SCS" ]]; then
		INS_GREP="MESSAGE"
	elif [[ $INS_TYPE = "ERS" ]]; then
		INS_GREP="ENQUE"		
	else
		INS_GREP="XXX"
	fi

	local STATUS=$(su - $1 -c "sapcontrol -nr $2 -function GetSystemInstanceList | grep $INS_GREP")
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
	export SID=$(echo ${nw_sid})
	export NR=$(echo ${nw_instance_number})
	export TYPE=$(echo ${nw_instance_type})

	export SIDADM=$(echo ${SID,,}adm)
	export HOSTNAME=$(uname -n)

	export STATUS=$(check_is_nw_up $SIDADM $NR $TYPE)

	return_ansible success

}

# For Ansible module, source $1 will take all the input parameters
source $1
main
