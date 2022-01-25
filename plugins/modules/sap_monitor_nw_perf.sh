#!/bin/bash
#   =====================================================================
# 
#	sap_monitor_nw_perf.sh
#	Authored by			-	Jason Masipiquena
#						-	IBM - Lab for SAP Solutions
#
#	Bash script designed to be used as an Ansible module
#	Checks SAP NW (PAS) performance metrics 
#	Input: 	
#		- nw_sid
# 		- nw_instance_number
#		- nw_instance_type
#	Output:
#		- heap_memory		-	Heap memory					-	access from Ansible via <register_variable>.heap_memory
#		- extended_memory	-	Extended memory				-	access from Ansible via <register_variable>.extended_memory
#		- cpu_util			-	CPU utilization				-	access from Ansible via <register_variable>.cpu_util
#		- program_swap		-	Program buffer swap			-	access from Ansible via <register_variable>.program_swap
#
#   =====================================================================

#   =====================================================================
#	Functions
#   =====================================================================
# 	get_heap_mem
#	get_ext_mem
#	get_cpu_util
#	get_program_buffer_swap
#	result_to_dictionary
#	return_ansible

# Returns SAP NW (PAS) heap memory
function get_heap_mem(){
	# $1 - NR
	local HEAPMEM=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep HeapAct | head -1 | awk '{ print $4 }')
	echo $HEAPMEM
}

# Returns SAP NW (PAS) extended memory
function get_ext_mem(){
	# $1 - NR
	local EXTMEM=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep EsAct | head -1 | awk '{ print $4 }')
	echo $EXTMEM
}

# Returns SAP NW (PAS) CPU utilization
function get_cpu_util(){
	# $1 - NR
	local CPUUTIL=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep CPU_Utilization | head -1 | awk '{ print $4 }')
	echo $CPUUTIL
}

# Returns SAP NW (PAS) program buffer swap
function get_program_buffer_swap(){
	# $1 - NR
	local PROGRAMSWAP=$(/usr/sap/hostctrl/exe/sapcontrol -nr $1 -function GetAlertTree | grep Program | grep Swap | head -1 | awk '{ print $4 }')
	echo $PROGRAMSWAP
}

# Process results to json format
function result_to_dictionary() {

	echo -n '{'
	
	echo -n \"HeapMemory\": \"${HEAPMEM//\"/\\\"}\"
	echo -n ', '
	echo -n \"ExtendedMemory\": \"${EXTMEM//\"/\\\"}\"
	echo -n ', '
	echo -n \"CpuUtil\": \"${CPUUTIL//\"/\\\"}\"
	echo -n ', '
	echo -n \"ProgramSwap\": \"${PROGRAMSWAP//\"/\\\"}\"
	
	echo -n '}'

}

# Return values for Ansible
function return_ansible(){

	local result=$1

	if [ $result = "success" ]; then
		printf '{"changed": %s, "failed": %s, "msg": "%s", "heap_memory": "%s", "extended_memory": "%s", "cpu_util": "%s", "program_swap": "%s"}' \
			false false "SAP Check $RETURN_MESSAGE" "$HEAPMEM" "$EXTMEM" "$CPUUTIL" "$PROGRAMSWAP" 
	else
		printf '{"changed": %s, "failed": %s, "msg": "%s", "heap_memory": "%s", "extended_memory": "%s", "cpu_util": "%s", "program_swap": "%s"}' \
			false true "SAP Check Failed" "$HEAPMEM" "$EXTMEM" "$CPUUTIL" "$PROGRAMSWAP" 
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

	export CPUUTIL=$(get_cpu_util $NR)
	export HEAPMEM=$(get_heap_mem $NR)
	export EXTMEM=$(get_ext_mem $NR)
	export PROGRAMSWAP=$(get_program_buffer_swap $NR)

	RESULTS_DICTIONARY=`result_to_dictionary`
	return_ansible success

}

# For Ansible module, source $1 will take all the input parameters
source $1
main
