# Supplementary information for sap_pyrfc Ansible Role

## Brief explanation of SAP RFCs

ABAP Function Modules interface parameters have different types:
- **Exporting parameters** = call the function module with parameter and data payload, the function module will use the data and provide a response (to the calling source/program). Always optional.
- **Importing parameters** = call the function module with parameter and data payload, the function module will use the data. Cannot be amended, may be required or optional.
- **Changing parameters** = call the function module with parameter and data payload, the function module will process the data and provide an amended response (to the calling source/program). May be required or optional.
- **Tables parameters** = call the function module with parameter and data payload with internal ABAP table data structures.

RFC parameters _(IMPORTING, EXPORTING, CHANGING)_ can accept the following data types:
- Data elements (string, integer)
- ABAP Structure
- ABAP Table

RFC parameters (TABLE) is deprecated and used for backwards compatibility, this can only accept one data type:
- ABAP Table

For futher information, refer to [ABAP Programming Language - Built-In Data Types - SAP NetWeaver AS ABAP 7.56](https://help.sap.com/doc/abapdocu_756_index_htm/7.56/en-us/abenbuilt_in_types_complete.htm).

## Context of SAP NWRFC SDK and PyRFC

For clarity, there are two SDKs for calling RFCs in SAP Systems which have been released by SAP:
1. [SAP NetWeaver Remote Function Call (RFC) Software Development Kit (SDK) (aka. "SAP NWRFC SDK")](https://support.sap.com/en/product/connectors/nwrfcsdk.html). `Supported by SAP`.
2. Classical "RFC SDK", previously bundled with the SAP Kernel and using ASCII ILE, EBCDIC ILE, UNICODE ILE, or PASE Unicode. `Deprecated as of SAP Kernel 7.41, on 2016-03-31`.

The SAP NetWeaver RFC SDK is a proprietary set of compiled binaries which provides a C/C++ interface for connecting to SAP Systems, enabling development of programs which call ABAP functionality (RFC clients) and programs which can be called from ABAP (RFC servers).

More details including a Programming Guide and Doxygen documentation can be found on [sap.com - connectors - nwrfcsdk](https://support.sap.com/en/product/connectors/nwrfcsdk.html)

Alternatives to the SAP NWRFC SDK include the SAP Java Connector (JCo), and SAP Connector for Microsoft .NET (NCo).

Optionally, the SAP NetWeaver RFC SDK can be called by multiple connectors/bindings for different runtime environments; which are released to open-source by SAP:
- Python: [PyRFC](https://github.com/SAP/PyRFC)
- Node.js: [node-rfc](https://github.com/SAP/node-rfc)
- Go: [gorfc](https://github.com/SAP/gorfc)

Other connectors/bindings to have previously existed but are infrequently used with the SAP NetWeaver RFC SDK are:
- R: [RSAP](https://github.com/piersharding/RSAP)
- Ruby: [ruby-sapnwrfc](https://github.com/piersharding/ruby-sapnwrfc)
- PHP 7/8: [php7-sapnwrfc](https://github.com/gkralik/php7-sapnwrfc)

### Samples from SAP NWRFC SDK

This additional context is to avoid confusion. By default the SAP NetWeaver RFC SDK includes two sample ALE programs (rfcexec or startrfc) as reference implementations which support the SAP IDoc scenario.

Neither of these sample programs are used by sap_pyrfc Ansible Role or the underlying PyRFC bindings.

These sample ALE programs appear in documentation available on help.sap.com under the IDoc Interface/ALE section:
- Using startrfc, [SAP NetWeaver AS - IDoc Interface/ALE - Inbound: Triggering the SAP System](https://help.sap.com/viewer/8f3819b0c24149b5959ab31070b64058/7.52.3/en-US/4b4c43dd3b71265ce10000000a421937.html)
- Using rfcexec, [SAP NetWeaver AS - IDoc Interface/ALE - Outbound: Triggering the Receiving System](https://help.sap.com/viewer/8f3819b0c24149b5959ab31070b64058/7.52.3/en-US/4b403cbe6f820a93e10000000a421937.html)
  - The rfcexec program is a generic RFC server and requires a forbidden/negative list for the operating system states which cannot be executed. A sample file 'rfcexec.sec' demonstrates those security configurations and is covered further in SAP Note 618516 - Security-related enhancement of RFCEXEC program.

## Security concerns with RFCs and SAP Systems

RFCs are very powerful, and with the wrong user privileges can be a security concern.

A useful RFC used by technical administrators is `RFC_ABAP_INSTALL_AND_RUN` which temporarily stores and executes an ABAP Report, which helps to demonstrate potential security concerns. This is now deprecated as of SAP S/4HANA 1809, as it could be used for arbitrary code execution onto SAP Systems.

**RFC_ABAP_INSTALL_AND_RUN workflow:**
- Call RFC with the PROGRAMNAME Importing Parameter (e.g. Z$$$XRFC), MODE Importing Parameter and ABAP Report to the PROGRAM Tables Parameter (with multiple Table Component called LINE and maximum 72 characters)
- Create temporary ABAP Report "Z$$$XRFC"
- Execute temporary ABAP Report "Z$$$XRFC"
- Store result of the executed ABAP Report into the WRITES Table Parameter
- Remove the temporary ABAP Report "Z$$$XRFC"
- Respond to the calling source/program with the WRITES Table Parameter or the ERRORMESSAGE Importing Parameter
