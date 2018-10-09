#!/bin/bash

###### Adjust to your local environment #####
RADIUS_SERVER=127.0.0.1
CLIENT_SECRET=mysecret
#####

# Read GET variables
saveIFS=$IFS
IFS='=&'
param=($QUERY_STRING)
IFS=$saveIFS

LOGIN=${param[1]}
PASS=${param[3]}

# Print form when login and password has not been provided
if [ -e $LOGIN -a -e $PASS ]; then
echo -n -e "Content-Type: text/html\n\n"

echo "<html><head><title>eduroam test</title></head><body>"

echo '<h2>eduroam test</h2>'
echo '<p>Provide just <b>TEST</b> credentials, do not entry credentials of real accounts.</p>'
echo '<p>Test tries EAP-PEAP MSCHAPv2 and EAP-TTLS PAP authentication.</p>'
echo '<p>No results and login/passwords are stored.</p>'

echo '<form action="eduroam-test.cgi" method="GET">'
echo 'Login: <input type="text" name="login"><br>'
echo 'Password: <input type="text" name="password"><br>'
echo '<input type="submit" value="Submit">'
echo '</form>'

echo '<p>Supported by CHAIN-REDS project and CESNET</p>'
printf '</body></html>'
exit
fi

# We have login and password, so do the test 
printf "Content-Type: text/html\n\n"
printf "<html><head><title>eduroam test</title></head><body>"
         
printf '<a href="#mschapv2">EAP-PEAP MSCHAPv2 results</a><br>'
printf '<a href="#pap">EAP-TTLS PAP results</a><br>'
             
# Unscape GET variables
LOGIN="$(perl -MURI::Escape -e 'print uri_unescape($ARGV[0]);' "$LOGIN")"
PASS="$(perl -MURI::Escape -e 'print uri_unescape($ARGV[0]);' "$PASS")"
    
printf '<a id="mschapv2"><h2>Testing EAP-PEAP MSCHAPv2</h2></a>'

TEMPLATE="network={\n
        ssid=\"eduroam\"\n
        key_mgmt=WPA-EAP\n 
        eap=PEAP\n
        identity=\"$LOGIN\"\n
        anonymous_identity=\"$LOGIN\"\n
        password=\"$PASS\"\n
        phase2=\"autheap=MSCHAPV2\"\n
}"

TMP_FILE=`mktemp --tmpdir=/dev/shm/`

echo -n -e $TEMPLATE > $TMP_FILE

printf "<h3>Configuration file used</h3>"

printf "<pre>\n"
cat $TMP_FILE
printf "</pre>\n"

TMP_OUT=`mktemp --tmpdir=/dev/shm/`
OUT=`/usr/local/bin/eapol_test -c $TMP_FILE -s $CLIENT_SECRET -a $RADIUS_SERVER 2>&1 >/${TMP_OUT}`
RET=$?

if [ $RET -ne 0 ] ;then
        RES='<span style="color: red;">FAILURE</span>'
else
        RES='<span style="color: green;">OK</span>'
fi

printf "<h3>Results of the test: $RES</h3>"

printf "<pre>\n"

cat $TMP_OUT

printf "</pre>\n"

rm $TMP_OUT
rm $TMP_FILE

printf '<a id="pap"><h2>Testing EAP-TTLS PAP</h2></a>'

TEMPLATE="network={\n
        ssid=\"eduroam\"\n
        key_mgmt=WPA-EAP\n
        eap=TTLS\n
        identity=\"$LOGIN\"\n
        anonymous_identity=\"$LOGIN\"\n
        password=\"$PASS\"\n
        phase2=\"auth=PAP\"\n
}"

TMP_FILE=`mktemp --tmpdir=/dev/shm/`

echo -n -e $TEMPLATE > $TMP_FILE

printf "<h3>Configuration file used</h3>"

printf "<pre>\n"
cat $TMP_FILE
printf "</pre>\n"

TMP_OUT=`mktemp --tmpdir=/dev/shm/`
OUT=`/usr/local/bin/eapol_test -c $TMP_FILE -s $CLIENT_SECRET -a $RADIUS_SERVER 2>&1 >/${TMP_OUT}`
RET=$?

if [ $RET -ne 0 ] ;then
        RES='<span style="color: red;">FAILURE</span>'
else
        RES='<span style="color: green;">OK</span>'
fi

printf "<h3>Results of the test: $RES</h3>"

printf "<pre>\n"

cat $TMP_OUT

printf "</pre>\n"

rm $TMP_OUT
rm $TMP_FILE

printf '</body></html>'
