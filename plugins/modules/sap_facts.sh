#!/bin/bash
#   =====================================================================
# 
#	sap_facts.sh
#	Authored by			-	Jason Masipiquena
#						-	IBM - Lab for SAP Solutions
#
#	Bash script designed to be used as an Ansible module
#	Gathers SAP facts in a host
#	- SAP HANA
#		- SIDs
#		- Instance Numbers (one per SID)
#	- SAP NW
#		- SIDs
#		- Instance Numbers (can be more than one per SID)
#		- Instance Types (ASCS, PAS, ERS, etc)
#	Input:
#		- params (all | nw | <SID> )
#	Output:
#		- sap_nw_sid	-	list of all SAP NW SIDs					-	access from Ansible via <register_variable>.sap_nw_sid
#		- sap_hana_sid	-	list of all SAP HANA SIDs				-	access from Ansible via <register_variable>.sap_hana_sid
#		- sap_nw_nr		-	list of all SAP NW instance numbers		-	access from Ansible via <register_variable>.sap_nw_nr
#		- sap_hana_nr	-	list of all SAP HANA instance numbers	-	access from Ansible via <register_variable>.sap_hana_nr
#		- sap_facts		-	dictionary list of all the details 		-	access from Ansible via <register_variable>.sap_facts
#
#   =====================================================================

#   =====================================================================
#	Functions
#   =====================================================================
#	get_all_hana_sid
#	get_all_nw_sid
#	get_sid_type
#	get_all_nw_nr
#	get_hana_nr
#	get_all_hana_nr
#	get_instance_type
#	check_sapstartsrv
#	start_sapstartsrv
#	check_sapcontrol
#	array_to_json
#	arrays_to_dictionary
#	process_final_results
#	return_ansible

# Loops through /hana/shared for all SIDs and exports results to global array HANA_SID_ARRAY
function get_all_hana_sid(){
	
	unset HANA_SID_ARRAY
	export HANA_SID_ARRAY
	
	if [ -d /hana/shared ]; then
		# /hana/shared directory exists
		while read LINE
		do
			### Check to see if /usr/sap/SID exists. If not then its probably not used anymore / its not a SID so ignore
			if [ -d /usr/sap/$LINE ]; then
				# $LINE is an HDB system
				HANA_SID_ARRAY+=( "$LINE" )
			else
				# $LINE not in /usr/sap
				:
			fi
		done < <(ls -1 /hana/shared)
		## process substitution otherwise the variable values wont appear outside loop
	else
		# /hana/shared directory doesnt exist
		unset HANA_SID_ARRAY
	fi

	# Check if HANA SID detected
	if [[ -z "${HANA_SID_ARRAY[@]}" ]]; then
		# HANA_SID_ARRAY is empty, no HANA SID found
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""HANA SID not found"
	else
		# Proceed with getting instance numbers
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""HANA SID found"
		get_all_hana_nr
	fi
}

# Loops through /sapmnt for all SIDs and exports results to global array NW_SID_ARRAY
function get_all_nw_sid(){
	
	unset NW_SID_ARRAY
	export NW_SID_ARRAY
	
	if [ -d /sapmnt ]; then
		# /sapmnt directory exists
		while read LINE
		do
			### Check to see if /usr/sap/SID exists. If not then its probably not used anymore / its not a SID so ignore
			if [ -d /usr/sap/$LINE ]; then
				# "$LINE is a SAP system"
				NW_SID_ARRAY+=( "$LINE" )
			else
				### Check to see if /sapmnt/SID/sap_bobj exists to see if its a bobj system
				if [ -d /sapmnt/$LINE/sap_bobj ]; then
					# $LINE is a bobj system
					NW_SID_ARRAY+=( "$LINE" )
				else
					# $LINE not a SID"
					:
				fi
			fi
		done < <(ls -1 /sapmnt)
		## process substitution otherwise the variable values wont appear outside loop
	else
		# /sapmnt directory doesnt exist
		unset NW_SID_ARRAY
	fi

	if [[ -z "${NW_SID_ARRAY[@]}" ]]; then
		# NW_SID_ARRAY is empty, no NW SID found
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""NW SID not found"
	else
		# Proceed with getting instance numbers
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""NW SID found"
		get_all_nw_nr
	fi
}

# Check SID if it's NW or HANA
function get_sid_type() {
	local PARAM=$1
	
	### Check to see if /usr/sap/SID exists. If not then its probably not used anymore / its not a SID so ignore
	if [ -d /hana/shared/$PARAM ]; then
		# $SID is an HDB system
		HANA_SID_ARRAY+=( "$PARAM" )
		RETURN_MESSAGE="- SID: $PARAM found - hana"
		get_all_hana_nr
	elif [ -d /sapmnt/$PARAM ]; then
		NW_SID_ARRAY+=( "$PARAM" )
		RETURN_MESSAGE="- SID: $PARAM found - nw"
		get_all_nw_nr
	else
		RETURN_MESSAGE="- SID: $PARAM not found"
		return_ansible failed
	fi

}

# Loops through NW_SID_ARRAY populated by function get_all_nw_sid and get NW instance numbers
function get_all_nw_nr(){
	
	unset NW_NR_ARRAY
	export NW_NR_ARRAY
	
	for i in "${NW_SID_ARRAY[@]}"
	do 
		SID=$(echo $i)
		SIDADM=${SID,,}adm
	
		while read LINE
		do
				
			## Get the first character and the last two characters
			LASTTWO=$(echo ${LINE: -2})
			FIRST=$(echo ${LINE:0:1})
			
			if [[ $LASTTWO =~ ^[0-9]+$ ]];then
				NR=$LASTTWO
				check_sapstartsrv $SIDADM $SID $NR
				sapcontrol_test=`check_sapcontrol $SIDADM $SID $NR`
				if [[ $sapcontrol_test == "fail" ]]; then
					# sapcontrol not working
					# invalid SAP system
					# ignore this instance number
					:
				else
					# sapcontrol is working
					# valid SAP system
					# add this instance number in NW_NR_ARRAY
					NW_NR_ARRAY+=( "$LASTTWO" )
				fi
			else
				:
			fi
		done < <(ls -1 /usr/sap/$SID)
	done

}

# Returns instance number of SAP HANA
function get_hana_nr(){
	# $1 - SID
	local NR=$(ls -1 /usr/sap/$1 | grep HDB | sed 's/...//' | head -1)
	HANA_NR_ARRAY+=( "$NR" )
}


# Loops through HANA_SID_ARRAY populated by function get_all_hana_sid and get HANA instance numbers
function get_all_hana_nr(){

	unset HANA_NR_ARRAY
	export HANA_NR_ARRAY
	
	for i in "${HANA_SID_ARRAY[@]}"
	do
		local SID=$(echo $i)
		local SIDADM=${SID,,}adm
		local NR=$(ls -1 /usr/sap/$SID | grep HDB | sed 's/...//' | head -1)
			
		check_sapstartsrv $SIDADM $SID $NR
		sapcontrol_test=`check_sapcontrol $SIDADM $SID $NR`
		if [[ $sapcontrol_test == "fail" ]]; then
			# sapcontrol not working
			# invalid SAP system
			# ignore this instance number
			:
		else
			# sapcontrol is working
			# valid SAP system
			# add this instance number in HANA_NR_ARRAY
			HANA_NR_ARRAY+=( "$NR" )
		fi
	done
}

# remove_failed_sids() {

# 	for target in "${NW_SID_ARRAY_DELETE[@]}"; do
# 		for i in "${!NW_SID_ARRAY[@]}"; do
# 			if [[ ${NW_SID_ARRAY[i]} = $target ]]; then
# 				unset 'NW_SID_ARRAY[i]'
# 			fi
# 		done
# 	done

# 	for target in "${HANA_SID_ARRAY_DELETE[@]}"; do
# 		for i in "${!HANA_SID_ARRAY[@]}"; do
# 			if [[ ${HANA_SID_ARRAY[i]} = $target ]]; then
# 				unset 'HANA_SID_ARRAY[i]'
# 			fi
# 		done
# 	done

# 	echo ${HANA_SID_ARRAY[@]}
# 	echo ${HANA_SID_ARRAY[@]}

# }

# Returns instance type of passed instance number
get_instance_type() {
	
	local INS=$1
	local FIRST=$(echo ${INS:0:1})
	local NR=""
	local INS_TYPE=""

	if [[ $FIRST = "D" ]]; then
		# It's a PAS
		INS_TYPE="PAS"
	elif [[ $FIRST = "A" ]]; then
		# It's an ASCS
		INS_TYPE="ASCS"
	elif [[ $FIRST = "W" ]]; then
		# It's a Webdisp
		INS_TYPE="WebDisp"
	elif [[ $FIRST = "J" ]]; then
		# It's a Java
		INS_TYPE="Java"
	elif [[ $FIRST = "S" ]]; then
		# It's an SCS
		INS_TYPE="SCS"
	elif [[ $FIRST = "E" ]]; then
		# It's an ERS
		INS_TYPE="ERS"		
	elif [[ $FIRST = "H" ]]; then
		# It's a HANA system
		INS_TYPE="HANA"	
	else
		# Unknown instance type
		INS_TYPE="XXX"
	fi
	
	echo $INS_TYPE

}

# Check if sapstartsrv is running
function check_sapstartsrv(){
	# $1 - SIDADM
	# $2 - SID
	# $3 - NR
	
	## Count the number of sapstartsrv processes
	SAPSTARTSRV=$(ps -ef | grep $2 | grep $3 | grep sapstartsrv | wc -l)
	
	if [[ $SAPSTARTSRV = 0 ]]; then
		## No sapstartsrv process running - attempt to start
		start_sapstartsrv $1 $2 $3
	elif [[ $SAPSTARTSRV -gt 1 ]]; then
		# Multiple sapstartsrv processes running for a given instance number
		# Stop all corresponding sapstartsrv processes
		for i in $SAPSTARTSRV
		do
			su - $1 -c "sapcontrol -nr $3 -function StopService $2"
		done
		# Start sapstartsrv
		start_sapstartsrv $1 $2 $3
	else
		# sapstartsrv is ok
		:
	fi
}

# Start sapstartsrv for given SID and NR
function start_sapstartsrv(){
	# $1 - SIDADM
	# $2 - SID
	# $3 - NR
	su - $1 -c "sapcontrol -nr $3 -function StartService $2"
}

# Check sapcontrol on an instance number
function check_sapcontrol(){
	# $1 - SIDADM
	# $2 - SID
	# $3 - NR
	local sapcontrol_test=`su - $1 -c "sapcontrol -nr $3 -function GetInstanceProperties"`
	if [[ $sapcontrol_test == *"FAIL"* ]]; then
		# sapcontrol not working
		echo "fail"
	else
		# sapcontrol is working
		echo "ok"
	fi
	
}

# Convert array to json format
function array_to_json() {
	echo -n '['
	while [ $# -gt 0 ]; do
		x=${1//\\/\\\\}
		echo -n \"${x//\"/\\\"}\"
		[ $# -gt 1 ] && echo -n ', '
		shift
	done
	echo ']'
}

# Convert all arrays to json dictionary format
function arrays_to_dictionary() {
	i=0
	echo -n '['
	
	while [ $# -gt 0 ]; do
		
		echo -n '{'
		
		x=${1//\\/\\\\}
		echo -n \"InstanceNumber\": \"${x//\"/\\\"}\"
		echo -n ', '
		echo -n \"InstanceType\": \"${DICT_ALL_INS_TYPE_ARRAY[i]//\"/\\\"}\"
		echo -n ', '
		echo -n \"SID\": \"${DICT_ALL_SID_ARRAY[i]//\"/\\\"}\"
		echo -n ', '
		echo -n \"Type\": \"${DICT_ALL_TYPE_ARRAY[i]//\"/\\\"}\"
		echo -n '}'

		[ $# -gt 1 ] && echo -n ', '
		
		shift
				
		i=$((i+1))
	done
	
	echo ']'

}

# Process results for Ansible
function process_final_results(){
	
	# Declare dictionary variables
	unset DICT_ALL_NR_ARRAY
	unset DICT_ALL_TYPE_ARRAY
	unset DICT_ALL_INS_TYPE_ARRAY
	unset DICT_ALL_SID_ARRAY
	unset DICT_ALL_NW_SID_ARRAY
	unset DICT_ALL_HANA_SID_ARRAY
	export DICT_ALL_NR_ARRAY
	export DICT_ALL_TYPE_ARRAY
	export DICT_ALL_INS_TYPE_ARRAY
	export DICT_ALL_SID_ARRAY
	export DICT_ALL_NW_SID_ARRAY
	export DICT_ALL_HANA_SID_ARRAY

	# Check NW and HANA arrays if empty
	if [[ -z "${HANA_NR_ARRAY[@]}" ]]; then
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""No valid HANA Systems found"
	else
		:
	fi

	if [[ -z "${NW_NR_ARRAY[@]}" ]]; then
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""No valid NW Systems found"
	else
		:
	fi

	if [[ -z "${NW_NR_ARRAY[@]}" ]] && [[ -z "${HANA_NR_ARRAY[@]}" ]]; then
		RETURN_MESSAGE="${RETURN_MESSAGE} - ""No valid Systems found"
	else
		:
	fi

	# Append all NW NR to final NR dictionary array
	for index in "${!NW_NR_ARRAY[@]}"
		do 
		DICT_ALL_NR_ARRAY+=( "${NW_NR_ARRAY[index]}" )
		DICT_ALL_TYPE_ARRAY+=( "nw" )
		done
	
	# Append all HANA NR to final NR dictionary array
	for index in "${!HANA_NR_ARRAY[@]}"
		do
		DICT_ALL_NR_ARRAY+=( "${HANA_NR_ARRAY[index]}" )
		DICT_ALL_TYPE_ARRAY+=( "hana" )
		done

	# Get instance information of all instance numbers
	for index in "${!DICT_ALL_NR_ARRAY[@]}"
		do
		
		local NR=$(echo ${DICT_ALL_NR_ARRAY[index]})
		local SID=$(/usr/sap/hostctrl/exe/sapcontrol -nr $NR -function GetInstanceProperties | grep SAPSYSTEMNAME | awk '{ print $3 }')
		local INS=$(/usr/sap/hostctrl/exe/sapcontrol -nr $NR -function GetInstanceProperties | grep INSTANCE_NAME | awk '{ print $3 }')
		
		# Get instance type
		local INS_TYPE=`get_instance_type $INS`
		
		DICT_ALL_INS_TYPE_ARRAY+=( "${INS_TYPE}" )

		if [[ ${INS_TYPE} == "HANA" ]]; then
			# Append all HANA SID
			DICT_ALL_HANA_SID_ARRAY+=( "${SID}" )
		else
			# Append all NW SID
			DICT_ALL_NW_SID_ARRAY+=( "${SID}" )
		fi
		
		# Append all SID
		DICT_ALL_SID_ARRAY+=( "${SID}" )

		done

	# Trim SID Arrays to get only unique SIDs
	IFS=" " read -r -a DICT_ALL_NW_SID_ARRAY <<< "$(tr ' ' '\n' <<< "${DICT_ALL_NW_SID_ARRAY[@]}" | sort -u | tr '\n' ' ')"
	IFS=" " read -r -a DICT_ALL_HANA_SID_ARRAY <<< "$(tr ' ' '\n' <<< "${DICT_ALL_HANA_SID_ARRAY[@]}" | sort -u | tr '\n' ' ')"

	# Process lists for all SIDs
	DICT_ALL_NW_SID_JSON=`array_to_json "${DICT_ALL_NW_SID_ARRAY[@]}"`
	DICT_ALL_HANA_SID_JSON=`array_to_json "${DICT_ALL_HANA_SID_ARRAY[@]}"`
	
	# Process lists for all NRs
	DICT_ALL_NW_NR_JSON=`array_to_json "${NW_NR_ARRAY[@]}"`
	DICT_ALL_HANA_NR_JSON=`array_to_json "${HANA_NR_ARRAY[@]}"`

	# Process dictionaries for sap_facts
	DICT_ALL_NR_JSON=`array_to_json "${DICT_ALL_NR_ARRAY[@]}"`
	DICT_ALL_SID_JSON=`array_to_json "${DICT_ALL_SID_ARRAY[@]}"`
	DICT_ALL_INS_TYPE_JSON=`array_to_json "${DICT_ALL_INS_TYPE_ARRAY[@]}"`
	DICT_ALL_TYPE_JSON=`array_to_json "${DICT_ALL_TYPE_ARRAY[@]}"`

	# Process all arrays for final json dictionary
	SAP_FACTS_DICTIONARY=`arrays_to_dictionary ${DICT_ALL_NR_ARRAY[@]}`

	# Return values for Ansible
	return_ansible success
		
}

# Return values for Ansible
function return_ansible(){

	local result=$1

	if [ $result = "success" ]; then
		printf '{"changed": %s, "failed": %s, "msg": "%s", "sap_nw_sid": %s, "sap_hana_sid": %s, "sap_nw_nr": %s, "sap_hana_nr": %s, "sap_facts": %s}' \
			false false "SAP Information Gathering Successful $RETURN_MESSAGE" "$DICT_ALL_NW_SID_JSON" "$DICT_ALL_HANA_SID_JSON"  "$DICT_ALL_NW_NR_JSON" "$DICT_ALL_HANA_NR_JSON" "$SAP_FACTS_DICTIONARY"
	else
		printf '{"changed": %s, "failed": %s, "msg": "%s", "sap_nw_sid": %s, "sap_hana_sid": %s, "sap_nw_nr": %s, "sap_hana_nr": %s, "sap_facts": %s}' \
			false true "SAP Information Gathering Failed $RETURN_MESSAGE" "$DICT_ALL_NW_SID_JSON" "$DICT_ALL_HANA_SID_JSON"  "$DICT_ALL_NW_NR_JSON" "$DICT_ALL_HANA_NR_JSON" "$SAP_FACTS_DICTIONARY"
	fi

	exit

}

#   =====================================================================
#	Main
#   =====================================================================
main () {

	# For blank input, default param="all"
	if [ -z "$param" ]; then
		param="all"
	fi

	if [ $param = "all" ]; then
		get_all_hana_sid
		get_all_nw_sid
	elif [ $param = "hana" ]; then
		get_all_hana_sid
	elif [ $param = "nw" ]; then
		get_all_nw_sid
	else
		# It must be a SID
		get_sid_type $param
	fi

	process_final_results

}

# For Ansible module, source $1 will take all the input parameters
source $1
main
