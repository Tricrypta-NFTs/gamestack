#!bin/bash
cd game-studio
p4 depot -t stream $1
p4 stream -t mainline //$1/main
mkdir -p ./P4_Workspaces/super_$1_main
cd ./P4_Workspaces/super_$1_main && p4 client -S //$1/main super_$1_main

cp ./p4d-files/.p4ignore ./P4_Workspaces/super_$1_main

p4 set P4CLIENT=super_$1_main
p4 add .p4ignore
p4 submit -d "add .p4ignore for ue5"

cd .. && p4 client -d super_$1_main && rm -r P4_Workspaces

