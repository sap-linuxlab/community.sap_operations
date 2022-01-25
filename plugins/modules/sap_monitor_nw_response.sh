#!/bin/bash
#   =====================================================================
# 
#	sap_monitor_nw_response.sh
#	Authored by			-	Jason Masipiquena
#						-	IBM - Lab for SAP Solutions
#
#	Bash script designed to be used as an Ansible module
#	Checks SAP NW (PAS) response times
#	Input: 	
#		- nw_sid
# 		- nw_instance_number
#		- nw_instance_type
#	Output:
#		- dialog_response_time		-	Dialog response time						-	access from Ansible via <register_variable>.dialog_response_time
#		- database_response_time	-	Database response time						-	access from Ansible via <register_variable>.database_response_time
#		- frontend_response_time	-	Front end response time						-	access from Ansible via <register_variable>.frontend_response_time
#		- number_users				-	Current number of users logged in			-	access from Ansible via <register_variable>.number_users
#
#   =====================================================================

#   =====================================================================
#	Functions
#   =====================================================================
# 	get_dia_resp
#	get_db_resp
#	get_front_resp
#	get_num_users
#	result_to_dictionary
#	return_ansible

# Returns SAP NW (PAS) dialog response time
function get_dia_resp(){
	# $1 - NR
	local DIARESP=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep ResponseTimeDialog | head -1 | awk '{ print $4 }')
	echo $DIARESP
}

# Returns SAP NW (PAS) database response time
function get_db_resp(){
	# $1 - NR
	local DBRESP=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep DBRequestTime | head -1 | awk '{ print $4 }')
	echo $DBRESP
}

# Returns SAP NW (PAS) front end response time
function get_front_resp(){
	# $1 - NR
	local FRONTRESP=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep FrontendResponseTime | head -1 | awk '{ print $4 }')
	echo $FRONTRESP
}

# Returns SAP NW (PAS) current number of logged in users
function get_num_users(){
	# $1 - NR
	local NUMUSERS=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep UsersLoggedIn | head -1 | awk '{ print $4 }')
	echo $NUMUSERS
}

# Process results to json format
function result_to_dictionary() {

	echo -n '{'
	
	echo -n \"DialogResponseTime\": \"${DIARESP//\"/\\\"}\"
	echo -n ', '
	echo -n \"DatabaseResponseTime\": \"${DBRESP//\"/\\\"}\"
	echo -n ', '
	echo -n \"FrontEndResponseTime\": \"${FRONTRESP//\"/\\\"}\"
	echo -n ', '
	echo -n \"NumberUsers\": \"${NUMUSERS//\"/\\\"}\"
	
	echo -n '}'

}

# Return values for Ansible
function return_ansible(){

	local result=$1

	if [ $result = "success" ]; then
		printf '{"changed": %s, "failed": %s, "msg": "%s", "dialog_response_time": "%s", "database_response_time": "%s", "frontend_response_time": "%s", "number_users": "%s"}' \
			false false "SAP Check $RETURN_MESSAGE" "$DIARESP" "$DBRESP" "$FRONTRESP" "$NUMUSERS" 
	else
		printf '{"changed": %s, "failed": %s, "msg": "%s", "dialog_response_time": "%s", "database_response_time": "%s", "frontend_response_time": "%s", "number_users": "%s"}' \
			false true "SAP Check Failed" "$DIARESP" "$DBRESP" "$FRONTRESP" "$NUMUSERS" 
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

	export DIARESP=$(get_dia_resp $NR)
	export DBRESP=$(get_db_resp $NR)
	export FRONTRESP=$(get_front_resp $NR)
	export NUMUSERS=$(get_num_users $NR)

	RESULTS_DICTIONARY=`result_to_dictionary`
	return_ansible success

}

# For Ansible module, source $1 will take all the input parameters
source $1
main
