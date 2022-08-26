#!bin/bash
cd game-studio
p4 depot -t stream $1
p4 stream -t mainline //$1/main
mkdir -p ./P4_Workspaces/$2_$1_main_c9
cd ./P4_Workspaces/$2_$1_main_c9 && p4 client -S //$1/main $2_$1_main_c9

cp ./p4d-files/.p4ignore ./P4_Workspaces/$2_$1_main_c9

p4 set P4CLIENT=$2_$1_main_c9
p4 add .p4ignore
p4 submit -d "add .p4ignore for ue5"

cd .. && p4 client -d $2_$1_main_c9 && rm -r P4_Workspaces

